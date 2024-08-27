from pydantic import BaseModel, Field
from typing import Optional, Mapping
from bson import ObjectId

from backend.models import ExternalLink, GameStats, GameCommonMeta


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)


class GameEntity(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str
    image: str
    description: str
    externalLinks: list[ExternalLink]
    stats: GameStats
    meta: Mapping[GameCommonMeta, any]


class UserEntity(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    username: str
    password_hash: str
    games_liked: list[PyObjectId] = Field(default_factory=list)
    # games_rated: Mapping[PyObjectId, int] = Field(default_factory=dict)
    games_played: list[PyObjectId] = Field(default_factory=list)

    @staticmethod
    async def get_user(db, username) -> 'UserEntity':
        return UserEntity(**(await db["users"].find_one({"username": username})))
