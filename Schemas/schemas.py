from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Any


class LocationBase(BaseModel):
    name: str
    latitude: float
    longitude: float


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    id: int
    reviews: List["LocationCategoryReviewed"] = []

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    reviews: List["LocationCategoryReviewed"] = []

    class Config:
        orm_mode = True


class LocationCategoryReviewedBase(BaseModel):
    location_id: int
    category_id: int
    last_reviewed: Optional[datetime]


class LocationCategoryReviewedCreate(LocationCategoryReviewedBase):
    pass


class LocationCategoryReviewed(LocationCategoryReviewedBase):
    id: int

    class Config:
        orm_mode = True


class LocationCategoryRecommendation(BaseModel):
    location: str
    category: str

    class Config:
        orm_mode = True


class ResponseModel(BaseModel):
    StatusCode: int
    response: Any

    class Config:
        orm_mode = True