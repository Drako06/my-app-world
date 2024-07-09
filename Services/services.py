from datetime import datetime, timedelta
from sqlalchemy.orm import Session
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

        # Obtener combinaciones que nunca se han revisado
        never_reviewed = db.query(Location, Category).outerjoin(
            LocationCategoryReviewed,
            (LocationCategoryReviewed.location_id == Location.id) &
            (LocationCategoryReviewed.category_id == Category.id)
        ).filter(LocationCategoryReviewed.id == None).limit(10).all()

        # Si hay menos de 10 combinaciones nunca revisadas, obtener combinaciones no revisadas en los últimos 30 días
        if len(never_reviewed) < 10:
            reviewed = db.query(LocationCategoryReviewed).filter(
                LocationCategoryReviewed.last_reviewed < thirty_days_ago
            ).order_by(LocationCategoryReviewed.last_reviewed).limit(10 - len(never_reviewed)).all()
            for review in reviewed:
                location = db.query(Location).filter(Location.id == review.location_id).first()
                category = db.query(Category).filter(Category.id == review.category_id).first()
                never_reviewed.append((location, category))

        return never_reviewed
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
