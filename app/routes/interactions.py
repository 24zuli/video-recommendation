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


# import random
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.models import UserInteraction, User, Video
# from datetime import datetime

# router = APIRouter()

# @router.post("/api/track-interaction")
# def track_interaction(user_id: int, video_id: int, interaction_type: str, db: Session = Depends(get_db)):
#     """
#     Store user interactions with videos (like, view, bookmark).
#     If a user doesn't exist, create them first.
#     """
#     user = db.query(User).filter(User.id == user_id).first()
#     video = db.query(Video).filter(Video.id == video_id).first()

#     if not user or not video:
#         return {"error": "User or Video not found"}

#     # Add interaction to database
#     interaction = UserInteraction(
#         user_id=user_id,
#         video_id=video_id,
#         interaction_type=interaction_type,
#         timestamp=datetime.utcnow()
#     )
#     db.add(interaction)
#     db.commit()
    
#     return {"message": "Interaction stored successfully"}

# @router.post("/api/generate-random-interactions")
# def generate_random_interactions(db: Session = Depends(get_db)):
#     """
#     Generate random user interactions to fill the database.
#     """
#     users = db.query(User).all()
#     videos = db.query(Video).all()
    
#     if not users or not videos:
#         return {"error": "No users or videos found in database"}

#     interaction_types = ["like", "view", "bookmark"]

#     for _ in range(500):  # Generate 500 random interactions
#         user = random.choice(users)
#         video = random.choice(videos)
#         interaction_type = random.choice(interaction_types)
        
#         interaction = UserInteraction(
#             user_id=user.id,
#             video_id=video.id,
#             interaction_type=interaction_type,
#             timestamp=datetime.utcnow()
#         )
#         db.add(interaction)

#     db.commit()
#     return {"message": "500 random interactions added"}
