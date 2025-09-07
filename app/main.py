from fastapi import FastAPI
from app.schemas.user_schema import Movie_Data
from app.db.db import engine, Base
from app.schemas.database_schemas import FeatureConfig, FeatureSpace, UserProfile
import uuid

app = FastAPI()

@app.on_event("startup")
def on_startup():
    # This will create tables if they don’t exist
    Base.metadata.create_all(bind=engine)

@app.post("/users/{user_id}")
async def update_user_db(user_id:uuid.UUID):
    # message = await update_data(user_id, movie_data)
    return {"message": "success"}