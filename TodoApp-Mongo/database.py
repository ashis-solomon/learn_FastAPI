from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pymongo import MongoClient

conn = MongoClient("mongodb+srv://ashissolomon24:Password%4024@cluster0.onimsgx.mongodb.net/?retryWrites=true&w=majority")


def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=="_id"}, **{i:a[i] for i in a if i!="_id"}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]

    
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {
        "check_same_thread": False
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()