import numpy as np
import tensorflow as tf
from tensorflow import keras
from sqlalchemy.orm import Session
from app.models import UserInteraction, Video

# Load pre-trained model (Ensure you train it first)
MODEL_PATH = "app/recommendation/recommendation_model.h5"
model = keras.models.load_model(MODEL_PATH) if tf.io.gfile.exists(MODEL_PATH) else None

def get_recommendations(user_id: int, db: Session):
    """
    Get ML-based video recommendations for a user.
    """
    if model is None:
        return {"error": "Recommendation model not trained yet."}
    
    # Get user interactions
    interactions = db.query(UserInteraction).filter(UserInteraction.user_id == user_id).all()
    if not interactions:
        return {"message": "No interactions found for this user. Showing popular videos."}
    
    # Extract watched video IDs
    watched_videos = [interaction.video_id for interaction in interactions]
    
    # Get all video IDs
    all_videos = db.query(Video).all()
    
    # Filter out already watched videos
    unseen_videos = [video.id for video in all_videos if video.id not in watched_videos]

    # Make predictions
    predictions = model.predict(np.array(unseen_videos))
    
    # Get top recommended video IDs
    top_recommendations = sorted(zip(unseen_videos, predictions.flatten()), key=lambda x: x[1], reverse=True)[:5]
    
    return [{"video_id": video_id, "score": score} for video_id, score in top_recommendations]
