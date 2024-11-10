from datetime import datetime

from pydantic import BaseModel


class ExternalLink(BaseModel):
    url: str
    img_url: str


class GameModel(BaseModel):
    id: str
    title: str
    description: str
    cover_image_url: str
    release_year: int
    external_links: list[ExternalLink]
    genres: list[str]
    developer: str
    publisher: str
    platforms: list[str]
    rating_esrb: str
    trailer_url: str
    likes: int
    ratings: list[int]


class NewGameModel(BaseModel):
    title: str
    description: str
    cover_image_url: str
    release_year: int
    external_links: list[ExternalLink]
    genres: list[str]
    platforms: list[str]
    developer: str
    publisher: str
    rating_esrb: str
    trailer_url: str


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
