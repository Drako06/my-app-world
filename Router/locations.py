from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.db_config import get_db
from Schemas.schemas import LocationCreate, ResponseModel
from Services import services


router = APIRouter()


@router.post("/", response_model=ResponseModel)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    try:
        response = services.create_location(db=db, location=location)

        return {
            "StatusCode": 200,
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

