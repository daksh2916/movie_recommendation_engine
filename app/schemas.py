from pydantic import BaseModel
import uuid

class Movie_Data(BaseModel):
    movieId: uuid.UUID
    title: str
    genres: str
    director: str
    actors: str
    production_house: str

    