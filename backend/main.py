from bson import ObjectId
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from backend.database.auth.auth import verify_password, get_password_hash
from backend.database.auth.security import get_user_from_token, create_access_token, validate_object_id
from backend.database.models import UserEntity
from backend.models import GameModel
from database.index import get_db
import motor.motor_asyncio

app = FastAPI()
load_dotenv()


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


# Users API
@app.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db)
):
    user = await UserEntity.get_user(db, form_data.username)
    if not user:
        return {"error": "User not found"}
    if not verify_password(form_data.password, user.password_hash):
        return {"error": "Incorrect password"}

    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register")
async def register(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db)
):
    user = await UserEntity.get_user(db, form_data.username)
    if user:
        return {"error": "User already exists"}

    new_user = UserEntity(username=form_data.username, password_hash=get_password_hash(form_data.password))

    result = await db.get_collection("users").insert_one(new_user.model_dump())
    if not result.acknowledged:
        return {"error": "Error creating user"}

    access_token = create_access_token(data={"sub": new_user.username})

    return {"access_token": access_token, "token_type": "bearer"}
