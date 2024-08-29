from pydantic import BaseModel, Field
from typing import Optional, Mapping, Any
from bson import ObjectId

from backend.models import ExternalLink, GameStats, GameCommonMeta, UserModel


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
    meta: Mapping[GameCommonMeta, Any]


class UserEntity(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    username: str
    password_hash: str
    profile_pic: str
    games_liked: list[PyObjectId] = Field(default_factory=list)
    games_rated: Mapping[str, int] = Field(default_factory=dict)
    games_played: list[PyObjectId] = Field(default_factory=list)

    @staticmethod
    async def get_user(db, username) -> Optional['UserEntity']:
        user = await db.get_collection("users").find_one({"username": username})
        if not user:
            return None
        return UserEntity(**user)

    def to_user_model(self) -> UserModel:
        user = self.model_dump()
        user["id"] = str(user.pop("id"))
        user.pop("password_hash")
        user["games_liked"] = [str(game) for game in user["games_liked"]]
        user["games_played"] = [str(game) for game in user["games_played"]]

        return UserModel(**user)
