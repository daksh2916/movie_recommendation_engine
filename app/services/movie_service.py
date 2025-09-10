from app.schemas.database_schemas import Movie
from app.db.db import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text
import json
import uuid


session: Session = SessionLocal()
db_name = session.execute(text("SELECT current_database()")).scalar()
print("🔎 FastAPI is writing to database:", db_name)

def add_movie_to_database():
    with open(r"C:\Users\anjut\Desktop\learn\recommendation_system\movies.json", "r", encoding="utf-8") as f:
        movies_data = json.load(f)

    movie_count = session.query(Movie).count()
    print(f"Current movie count in database: {movie_count}")

    if movie_count > 0:
        session.close()
        print("Movies already initialized.")
        return {"message": "Movies already initialized."}
    
    for movie_info in movies_data:
        movie = Movie(
            id=uuid.UUID(movie_info["id"]),
            title=movie_info["title"],
            genres=movie_info["genres"],
            director=movie_info["director"],
            actors=movie_info["actors"],
            production_house=movie_info["production_house"],
            release_year=movie_info.get("release_year")
        )
        session.add(movie)

    session.commit()
    session.close()
    print("✅ Movies added to the database")