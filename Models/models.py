from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.db_config import Base
from datetime import datetime


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    reviews = relationship("LocationCategoryReviewed", back_populates="location")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    reviews = relationship("LocationCategoryReviewed", back_populates="category")


class LocationCategoryReviewed(Base):
    __tablename__ = "location_category_reviewed"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    last_reviewed = Column(DateTime, default=datetime.utcnow)

    location = relationship("Location", back_populates="reviews")
    category = relationship("Category", back_populates="reviews")
