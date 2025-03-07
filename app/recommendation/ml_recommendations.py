from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.recommendation.recommendation_model import get_recommendations

router = APIRouter()

@router.get("/ml-recommend")
def get_ml_recommendations(user_id: int, db: Session = Depends(get_db)):
    """
    Returns ML-based recommendations for a user.
    """
    recommendations = get_recommendations(user_id, db)
    return {"recommendations": recommendations}
