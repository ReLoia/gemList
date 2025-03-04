import json

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import os

if not os.path.exists('./data'):
    os.makedirs('./data')

DATABASE_URL = "sqlite:///./data/backend.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from backend.models import UserModel, GameModel

games_liked = Table(
    "games_liked",
    Base.metadata,
    Column("user_id", Integer, sqlalchemy.ForeignKey("users.id"), primary_key=True),
    Column("game_id", Integer, sqlalchemy.ForeignKey("games.id"), primary_key=True)
)

games_played = Table(
    "games_played",
    Base.metadata,
    Column("user_id", Integer, sqlalchemy.ForeignKey("users.id"), primary_key=True),
    Column("game_id", Integer, sqlalchemy.ForeignKey("games.id"), primary_key=True)
)


class GameEntity(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    cover_image_url = Column(String)
    release_year = Column(Integer)
    external_links = Column(String)  # Stored as JSON
    genres = Column(String)  # Stored as JSON
    developer = Column(String)
    publisher = Column(String)
    platforms = Column(String)  # Stored as JSON
    rating_esrb = Column(String)
    trailer_url = Column(String)
    likes = Column(Integer)
    ratings = Column(String)  # Stored as JSON

    @staticmethod
    def get_game(db, game_id: int):
        return db.query(GameEntity).get(game_id)

    @staticmethod
    def get_all_by_publisher(db, publisher: str):
        return db.query(GameEntity).filter(GameEntity.publisher == publisher).all()

    def get_all_by_same_publisher(self, db):
        return db.query(GameEntity).filter(GameEntity.publisher == self.publisher).filter(
            GameEntity.id != self.id).all()

    def to_game_model(self):
        return GameModel(
            id=str(self.id),
            title=self.title,
            description=self.description,
            cover_image_url=self.cover_image_url,
            release_year=self.release_year,
            external_links=json.loads(self.external_links),
            genres=json.loads(self.genres),
            developer=self.developer,
            publisher=self.publisher,
            platforms=json.loads(self.platforms),
            rating_esrb=self.rating_esrb,
            trailer_url=self.trailer_url,
            likes=self.likes,
            ratings=json.loads(self.ratings)
        )


class UserEntity(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    creation_date = Column(DateTime)
    profile_pic = Column(String)
    games_liked = relationship("GameEntity", secondary=games_liked)
    games_rated = Column(String)  # Stored as JSON
    games_played = relationship("GameEntity", secondary=games_played)

    @staticmethod
    def get_user(db, username: str):
        return db.query(UserEntity).filter(UserEntity.username == username).first()

    def to_user_model(self):
        return UserModel(
            id=self.id,
            username=self.username,
            profile_pic=self.profile_pic,
            creation_date=self.creation_date,
            games_liked=[str(game.id) for game in self.games_liked],
            games_rated=json.loads(self.games_rated),
            games_played=[str(game.id) for game in self.games_played]
        )

    def rate_game(self, game_id: int, rating: int):
        user_rated_games = json.loads(self.games_rated)
        user_rated_games[str(game_id)] = rating
        self.games_rated = json.dumps(user_rated_games)

    def has_liked_game(self, game_id: int):
        return any(game.id == game_id for game in self.games_liked)

    def like_game(self, db, game_id: int):
        if self.has_liked_game(game_id):
            self.games_liked.remove(GameEntity.get_game(db, game_id))
        else:
            self.games_liked.append(GameEntity.get_game(db, game_id))


Base.metadata.create_all(bind=engine)
