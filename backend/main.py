from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

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
        search_filter: str = "recent",
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db)
):
    games_collection = db.get_collection("games")

    match search_filter:
        case "recent":
            games = await games_collection.find().sort([("meta.releaseYear", -1)]).to_list(40)
        case "popular":
            games = await games_collection.find().sort([("stats.likes", -1)]).to_list(40)
        case _:
            games = await games_collection.find().to_list(40)

    for game in games:
        game["id"] = str(game.pop("_id"))

    print(games)

    return games


@app.get("/game/{game_id}")
async def get_game(
        game_id: int,
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db)
):
    games_collection = db.get_collection("games")
    game = await games_collection.find_one({"_id": game_id})
    return game
