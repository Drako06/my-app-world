from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc
from fastapi import HTTPException, status
from Models.models import Location, Category, LocationCategoryReviewed
from Schemas.schemas import LocationCreate, CategoryCreate, LocationCategoryReviewedCreate


def create_location(db: Session, location: LocationCreate) -> Location:
    try:
        db_location = Location(name=location.name, latitude=location.latitude, longitude=location.longitude)
        db.add(db_location)
        db.commit()
        db.refresh(db_location)
        return db_location
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def create_category(db: Session, category: CategoryCreate) -> Category:
    try:
        db_category = Category(name=category.name)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def create_location_category_reviewed(db: Session, location_category_reviewed: LocationCategoryReviewedCreate) -> LocationCategoryReviewed:
    try:
        db_reviewed = LocationCategoryReviewed(**location_category_reviewed.dict())
        db.add(db_reviewed)
        db.commit()
        db.refresh(db_reviewed)
        return db_reviewed
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def get_recommendations(db: Session):
    try:
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recommendations = db.query(
            Location, Category
        ).join(
            LocationCategoryReviewed, Location.id == LocationCategoryReviewed.location_id
        ).join(
            Category, Category.id == LocationCategoryReviewed.category_id
        ).filter(
            or_(
                LocationCategoryReviewed.last_reviewed < thirty_days_ago,
                LocationCategoryReviewed.last_reviewed.is_(None)
            )
        ).order_by(
            asc(LocationCategoryReviewed.last_reviewed.isnot(None)),
            LocationCategoryReviewed.last_reviewed
        ).limit(10).all()
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
