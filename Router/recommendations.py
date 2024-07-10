from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Services import services
from db.db_config import get_db
from typing import Dict, Any

router = APIRouter()


@router.get("/recommendations/", response_model=Dict[str, Any])
def read_recommendations(db: Session = Depends(get_db)):
    try:
        recommendations = services.get_recommendations(db)
        response_data = [
            {
                "location": recommendation[0].name,
                "category": recommendation[1].name
            } for recommendation in recommendations
        ]
        return {
            "StatusCode": 200,
            "response": response_data
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))