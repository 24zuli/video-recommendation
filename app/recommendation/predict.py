import numpy as np
import tensorflow as tf
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import UserInteraction, Video

MODEL_PATH = "app/recommendation/recommendation_model.keras"


def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

def get_recommendations(user_id: int, db: Session):
    model = load_model()

    all_videos = db.query(Video).all()
    video_ids = np.array([video.id for video in all_videos])

    if video_ids.size == 0:
        return {"user_id": user_id, "recommended_videos": []}

    predictions = model.predict(video_ids.reshape(-1, 1))


    recommended_videos = sorted(zip(video_ids, predictions.flatten()), key=lambda x: x[1], reverse=True)

    top_videos = [int(video[0]) for video in recommended_videos[:5]]

    return {"user_id": user_id, "recommended_videos": top_videos}
