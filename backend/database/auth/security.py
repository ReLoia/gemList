import jwt
from datetime import datetime, timedelta, UTC
import os
import motor.motor_asyncio
from bson import ObjectId

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from backend.database.index import get_db
from backend.database.models import UserEntity

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("jwt_secret", "beppe")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user_from_token(token: str = Depends(oauth2_scheme),
                              db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db)) -> 'UserEntity':
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = await UserEntity.get_user(db, username)
    if user is None:
        raise credentials_exception
    return user


def validate_object_id(obj_id: str):
    """
    Validate the obj_id for FastAPI and convert it to ObjectId.
    If the obj_id is not valid, it will raise a FastAPI HTTPException.
    :param obj_id:
    :return:
    """
    if not ObjectId.is_valid(obj_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    return ObjectId(obj_id)
