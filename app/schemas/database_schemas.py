from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, ARRAY, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.db import Base
import uuid

class FeatureConfig(Base):
    __tablename__ = "feature_config"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version = Column(Integer, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship: one config -> many features
    features = relationship("FeatureSpace", back_populates="config")

class FeatureSpace(Base):
    __tablename__ = "feature_space"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    config_id = Column(UUID(as_uuid=True), ForeignKey("feature_config.id"))
    category = Column(String, nullable=False)  
    name = Column(String, nullable=False)      # e.g., "Thriller", "Nolan"
    position = Column(Integer, nullable=False) # position in vector

    # Backlink
    config = relationship("FeatureConfig", back_populates="features")


# 3. User Profiles (vector per user per version)
class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    config_id = Column(UUID(as_uuid=True), ForeignKey("feature_config.id"))
    preferences = Column(ARRAY(Integer))  # vector of integers
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Movie(Base):
    __tablename__ = "movies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    genres = Column(ARRAY(String), nullable=False)
    director = Column(String, nullable=False)
    actors = Column(ARRAY(String), nullable=False)
    production_house = Column(String, nullable=False)
    release_year = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
