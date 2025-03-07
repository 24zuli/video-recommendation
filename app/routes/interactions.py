from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import UserInteraction, User, Video

router = APIRouter()

# ✅ Define a request model for input validation
class InteractionRequest(BaseModel):
    user_id: int
    video_id: int
    interaction_type: str  # Should be 'view', 'like', 'bookmark', etc.

@router.post("/track-interaction")
def track_interaction(request: InteractionRequest, db: Session = Depends(get_db)):
    """
    Track user interactions with videos (like, view, bookmark).
    """
    # ✅ Check if user exists
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        print(f"User ID {request.user_id} NOT found in DB")  # Debugging
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Check if video exists
    video = db.query(Video).filter(Video.id == request.video_id).first()
    if not video:
        print(f"Video ID {request.video_id} NOT found in DB")  # Debugging
        raise HTTPException(status_code=404, detail="Video not found")

    # ✅ Store interaction
    interaction = UserInteraction(
        user_id=request.user_id,
        video_id=request.video_id,
        interaction_type=request.interaction_type
    )
    db.add(interaction)
    db.commit()

    return {"message": "Interaction stored successfully"}

