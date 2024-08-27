from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from database.index import get_db
import motor.motor_asyncio

app = FastAPI()
load_dotenv()


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/game/{game_id}")
async def get_game(
        game_id: int,
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db)
):
    games_collection = db.get_collection("games")
    game = await games_collection.find_one({"_id": game_id})
    return game
