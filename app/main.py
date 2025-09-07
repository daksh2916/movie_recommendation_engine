from fastapi import FastAPI
from app.schemas.user_schema import Movie_Data
from app.db.db import engine, Base
from app.schemas.database_schemas import FeatureConfig, FeatureSpace, UserProfile
from app.services.feature_service import init_features
from app.db.vector_db import vector_db_status
import uuid

app = FastAPI()

@app.on_event("startup")
def on_startup():
    # This will create tables if they don’t exist
    Base.metadata.create_all(bind=engine)
    init_features()
    vector_db_status_message = vector_db_status()
    print("Vector DB Status:", vector_db_status_message)

    
@app.post("/users/{user_id}")
async def update_user_db(user_id:uuid.UUID):
    # message = await update_data(user_id, movie_data)
    return {"message": "success"}