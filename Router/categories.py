from fastapi import APIRouter, Depends, HTTPException, status
from Schemas.schemas import CategoryCreate, ResponseModel
from sqlalchemy.orm import Session
from Services import services
from db.db_config import get_db


router = APIRouter()


@router.post("/categories/", response_model=ResponseModel)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        response = services.create_category(db=db, category=category)
        return {
            "StatusCode": 200,
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))