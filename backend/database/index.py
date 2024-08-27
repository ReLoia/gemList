import os
from typing import Mapping, Any
import motor.motor_asyncio


class MongoDBClientSingleton:
    _instance = None
    _client: motor.motor_asyncio.AsyncIOMotorClient[Mapping[str, Any]] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if self._client is None:
            self._client = motor.motor_asyncio.AsyncIOMotorClient(
                f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASS')}@{os.getenv('MONGO_HOST')}/test?retryWrites=true&w=majority&appName=gemlist"
            )

    def get_database(self, db_name: str):
        return self._client.get_database(db_name)


def get_db():
    return MongoDBClientSingleton().get_database("gemlist")
