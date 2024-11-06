from datetime import datetime

from pydantic import BaseModel


class GameModel(BaseModel):
    id: str
    title: str
    image: str
    description: str
    external_links: list[dict]
    stats: dict
    meta: dict
    release_year: int
    likes: int


class NewGameModel(BaseModel):
    title: str
    image: str
    description: str
    external_links: list[dict]
    stats: dict
    meta: dict
    release_year: int


class UserModel(BaseModel):
    username: str
    profile_pic: str
    creation_date: datetime
    games_liked: list[str]
    games_rated: dict[str, int]  # game_id: rating
    games_played: list[str]


class NewPasswordModel(BaseModel):
    old_password: str
    new_password: str
