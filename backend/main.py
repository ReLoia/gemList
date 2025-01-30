import json
import os
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.database.auth.auth import verify_password, get_password_hash
from backend.database.auth.security import get_user_from_token, create_access_token
from backend.database.models import UserEntity, GameEntity
from backend.database.session import get_db
from backend.models import GameModel, UserModel, NewGameModel, NewPasswordModel, GameRating

origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://gem-list.vercel.app",
    os.getenv("FRONTEND_URL", "")
]

ROOT_PATH = os.environ.get("ROOT_PATH", "")

app = FastAPI(
    title="GemList API",
    description="API for gemList",
    version="1.0",
    root_path=ROOT_PATH
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
    return RedirectResponse(url=f"{ROOT_PATH}/docs")


@app.get("/games", response_model=list[GameModel])
async def get_games(
        sort: str = "recent",
        db: Session = Depends(get_db)
):
    if sort == "recent":
        games = db.query(GameEntity).order_by(GameEntity.release_year.desc()).limit(40).all()
    elif sort == "popular":
        games = db.query(GameEntity).order_by(GameEntity.likes.desc()).limit(40).all()
    else:
        games = db.query(GameEntity).limit(40).all()

    return [game.to_game_model().model_dump() for game in games]


@app.get("/games/{game_id}", response_model=GameModel)
async def get_game(
        game_id: int,
        db: Session = Depends(get_db)
):
    game = GameEntity.get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game.to_game_model().model_dump()


@app.post("/games/{game_id}/rate")
async def rate_game(
        game_id: int,
        value: GameRating,
        user: UserEntity = Depends(get_user_from_token),
        db: Session = Depends(get_db)
):
    rating = value.rating
    if rating not in range(1, 11) or not isinstance(rating, int):
        raise HTTPException(status_code=400, detail="Rating must be an integer between 1 and 10")

    game: GameEntity = db.query(GameEntity).get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    user_rating = user.to_user_model().games_rated.get(str(game_id))

    game_ratings_parsed = json.loads(game.ratings)

    if user_rating:
        game_ratings_parsed[user_rating - 1] -= 1

    game_ratings_parsed[rating - 1] += 1

    game.ratings = json.dumps(game_ratings_parsed)

    user.rate_game(game_id, rating)

    db.commit()
    return {"message": "Rating updated"}


@app.post("/games/{game_id}/like")
async def like_game(
        game_id: int,
        user: UserEntity = Depends(get_user_from_token),
        db: Session = Depends(get_db)
):
    game = db.query(GameEntity).get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    user_has_liked = user.has_liked_game(game_id)

    if user_has_liked:
        game.likes -= 1
    else:
        game.likes += 1

    user.like_game(db, game_id)

    db.commit()
    return {"message": "Game liked" if not user_has_liked else "Game unliked"}


@app.post("/games/get", response_model=list[GameModel])
async def get_games_from_ids(
        game_ids: list[int],
        db: Session = Depends(get_db)
):
    games = db.query(GameEntity).filter(GameEntity.id.in_(game_ids)).all()
    return [game.to_game_model().model_dump() for game in games]


@app.get("/games/{game_id}/same-publisher", response_model=list[GameModel])
async def get_games_same_publisher(
        game_id: int,
        db: Session = Depends(get_db)
):
    game = db.query(GameEntity).get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    games = game.get_all_by_same_publisher(db)
    return [game.to_game_model().model_dump() for game in games]


# TODO: remove
@app.post("/games", response_model=GameModel, status_code=201)
async def add_game(
        game: NewGameModel,
        user: UserEntity = Depends(get_user_from_token),
        db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not user.username == "reloia":
        raise HTTPException(status_code=403, detail="Forbidden")

    new_game = GameEntity(
        title=game.title,
        description=game.description,
        cover_image_url=game.cover_image_url,
        release_year=game.release_year,
        external_links=json.dumps(list(map(lambda x: x.model_dump(), game.external_links))),
        genres=json.dumps(game.genres),
        developer=game.developer,
        publisher=game.publisher,
        platforms=json.dumps(game.platforms),
        rating_esrb=game.rating_esrb,
        trailer_url=game.trailer_url,
        likes=0,
        ratings=json.dumps([0] * 10)
    )
    db.add(new_game)
    db.commit()
    return new_game.to_game_model().model_dump()


# Auth


@app.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = UserEntity.get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=404, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register")
async def register(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = UserEntity.get_user(db, form_data.username)
    if user:
        raise HTTPException(status_code=409, detail="User already exists")

    new_user = UserEntity(
        username=form_data.username,
        password_hash=get_password_hash(form_data.password),
        creation_date=datetime.now(),
        profile_pic="",
        games_rated="{}"
    )
    db.add(new_user)
    db.commit()

    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=UserModel)
async def get_user(
        user: UserEntity = Depends(get_user_from_token)
):
    return user.to_user_model().model_dump()


@app.get("/users/me/rating/{game_id}")
async def get_user_rating(
        game_id: int,
        user: UserEntity = Depends(get_user_from_token)
):
    return user.to_user_model().games_rated.get(str(game_id))


@app.get("/users/me/liked/{game_id}")
async def get_user_liked(
        game_id: int,
        user: UserEntity = Depends(get_user_from_token)
):
    return user.has_liked_game(game_id)


@app.post("/users/me/change-password")
async def change_password(
        new_data: NewPasswordModel,
        user: UserEntity = Depends(get_user_from_token),
        db: Session = Depends(get_db)
):
    if not verify_password(new_data.old_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    user.password_hash = get_password_hash(new_data.new_password)

    db.commit()
    return {"message": "Password changed"}
