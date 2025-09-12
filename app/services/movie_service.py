from app.schemas.database_schemas import Movie
from app.db.db import SessionLocal
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
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

def make_embedding_text(movie):
    return f"""
    Title: {movie['title']}
    Genres: {', '.join(movie['genres'])}
    Director: {movie['director']}
    Actors: {', '.join(movie['actors'])}
    Production House: {movie['production_house']}
    Release Year: {movie['release_year']}
    """

def add_movies_to_vector_db():
    with open(r"C:\Users\anjut\Desktop\learn\recommendation_system\movies.json", "r", encoding="utf-8") as f:
        movies_data = json.load(f)

    print(f"Total movies to add to vector DB: {len(movies_data)}")
    
    model = SentenceTransformer("all-MiniLM-L6-v2")

    pc = Pinecone(
    api_key="pcsk_2GAsiz_3bdcQBwRNcpEaAKddukkmKpNxsRrYUoakMNNQbrTcGCccnwHdudWrSb3Aj4S2hn",
    )

    index_name = "movie-embeddings"

    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

    index = pc.Index(index_name)
    
    new_vectors = []
    for m in movies_data:
        # Check if this movie ID already exists
        existing = index.fetch(ids=[m["id"]])

        if existing.vectors:  # FetchResponse has .vectors dict
            print(f"⚠️ Skipping {m['title']} (already exists)")
            continue

        # Create embedding
        text = make_embedding_text(m)
        embedding = model.encode(text).tolist()

        new_vectors.append({
            "id": m["id"],
            "values": embedding,
            "metadata": {
                "title": m["title"],
                "director": m["director"],
                "genres": m["genres"],
                "production_house": m["production_house"],
                "release_year": m["release_year"]
            }
        })

    # Bulk insert only new movies
    if new_vectors:
        index.upsert(vectors=new_vectors)
        print(f"✅ {len(new_vectors)} new movies added to Pinecone")
    else:
        print("✅ No new movies to insert")