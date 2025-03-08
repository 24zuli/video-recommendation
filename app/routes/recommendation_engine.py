from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.recommendation.predict import get_recommendations

router = APIRouter()

@router.get("/recommend-engine")
def recommend_videos(user_id: int, db: Session = Depends(get_db)):
    """
    Get video recommendations for a user.
    """
    recommendations = get_recommendations(user_id, db)

    if not recommendations["recommended_videos"]:
        raise HTTPException(status_code=404, detail="No recommendations available")
    
    recommendations["recommended_videos"] = [int(video) for video in recommendations["recommended_videos"]]

    return recommendations
