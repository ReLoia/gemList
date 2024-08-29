from bson import ObjectId
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from backend.database.auth.auth import verify_password, get_password_hash
from backend.database.auth.security import get_user_from_token, create_access_token, validate_object_id
from backend.database.models import UserEntity, UserModel
from backend.models import GameModel
from backend.database.index import get_db
import motor.motor_asyncio

origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://gem-list.vercel.app"
]

app = FastAPI(
    title="GemList API",
    description="API for gemList",
    version="1.0"
)
load_dotenv()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/games",
         summary="Get all games",
         response_description="List of games",
         response_model=list[GameModel])
async def get_games(
        sort: str = "recent",
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db)
):
    games_collection = db.get_collection("games")

    match sort:
        case "recent":
            games = await games_collection.find().sort([("meta.releaseYear", -1)]).to_list(40)
        case "popular":
            games = await games_collection.find().sort([("stats.likes", -1)]).to_list(40)
        case _:
            games = await games_collection.find().to_list(40)

    for game in games:
        game["id"] = str(game.pop("_id"))

    return games


@app.get("/games/{game_id}", response_model=GameModel)
async def get_game(
        game_id: str = Depends(validate_object_id),
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db)
):
    games_collection = db.get_collection("games")
    game = await games_collection.find_one({"_id": ObjectId(game_id)})
    return {"id": str(game.pop("_id")), **game}


@app.post("/games/{game_id}/rate")
async def rate_game(
        game_id: str = Depends(validate_object_id),
        rating: int = -1,
        user: UserEntity = Depends(get_user_from_token),
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db)
):
    """
    game["stats"]["rating"] is an array of ratings form 1 to 10 (0-9)
    so if the user rates 5, we need to increment the 4th index
    if the user rates a number outside the range or a float, we return an error

    """
    # TODO: make edits on the user entity when the user rates a game

    if rating not in range(1, 11):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 10")

    if not isinstance(rating, int):
        raise HTTPException(status_code=400, detail="Rating must be an integer")

    games_collection = db.get_collection("games")
    user_collection = db.get_collection("users")

    game = await games_collection.find_one({"_id": game_id})
    game_ratings = game["stats"]["ratings"]

    # check if the user has already rated the game, if he has, update the rating
    if str(game_id) in user.games_rated:
        old_rating = user.games_rated[str(game_id)]
        game_ratings[old_rating - 1] -= 1

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    game_ratings[rating - 1] += 1

    await games_collection.update_one({"_id": game_id}, {"$set": {"stats.ratings": game_ratings}})
    await user_collection.update_one({"_id": user.id}, {"$set": {"games_rated": {str(game_id): rating}}})

    return {"message": "Rating updated"}


@app.post("/games/{game_id}/like")
async def like_game(
        game_id: str = Depends(validate_object_id),
        user: UserEntity = Depends(get_user_from_token),
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db)
):
    games_collection = db.get_collection("games")
    user_collection = db.get_collection("users")
    game = await games_collection.find_one({"_id": game_id})

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    game_likes = game["stats"]["likes"]
    game_likes += 1

    await games_collection.update_one({"_id": game_id}, {"$set": {"stats.likes": game_likes}})
    await user_collection.update_one({"_id": user.id}, {"$push": {"games_liked": game_id}})

    return {"message": "Game liked"}


@app.post("/games/get")
async def get_games_from_ids(
        game_ids: list[str],
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db)
):
    for game_id in game_ids:
        if not ObjectId.is_valid(game_id):
            raise HTTPException(status_code=400, detail="Invalid ObjectId")

    games_collection = db.get_collection("games")
    games = await games_collection.find({"_id": {"$in": [ObjectId(game_id) for game_id in game_ids]}}).to_list(40)

    for game in games:
        game["id"] = str(game.pop("_id"))

    return games


# Users API
@app.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db)
):
    user = await UserEntity.get_user(db, form_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register")
async def register(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db)
):
    user = await UserEntity.get_user(db, form_data.username)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = UserEntity(username=form_data.username, password_hash=get_password_hash(form_data.password),
                          profile_pic="", games_liked=[], games_rated={}, games_played=[])

    result = await db.get_collection("users").insert_one(new_user.model_dump())
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to register user")

    access_token = create_access_token(data={"sub": new_user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=UserModel)
async def get_user(
        user: UserEntity = Depends(get_user_from_token),
):
    # TODO: load every game the user has liked, rated and played
    return user.to_user_model()
