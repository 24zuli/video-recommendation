# import numpy as np
# import tensorflow as tf
# from sqlalchemy.orm import Session
# from app.database import SessionLocal
# from app.models import UserInteraction, Video

# MODEL_PATH = "app/recommendation/recommendation_model.keras"

# # ✅ Load the trained model
# def load_model():
#     return tf.keras.models.load_model(MODEL_PATH)

# def get_recommendations(user_id: int, db: Session = SessionLocal()):
#     model = load_model()

#     # Get all video IDs
#     all_videos = db.query(Video).all()
#     video_ids = np.array([video.id for video in all_videos])

#     # Predict scores for each video
#     predictions = model.predict(video_ids)

#     # Sort videos based on recommendation score
#     recommended_videos = sorted(zip(video_ids, predictions.flatten()), key=lambda x: x[1], reverse=True)

#     # Return top 5 recommendations
#     top_videos = [video[0] for video in recommended_videos[:5]]
    
#     return {"user_id": user_id, "recommended_videos": top_videos}

import numpy as np
import tensorflow as tf
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import UserInteraction, Video

MODEL_PATH = "app/recommendation/recommendation_model.keras"

# ✅ Load the trained model
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

def get_recommendations(user_id: int, db: Session):
    model = load_model()

    # Get all video IDs
    all_videos = db.query(Video).all()
    video_ids = np.array([video.id for video in all_videos])

    # ✅ Handle edge case: No videos available
    if video_ids.size == 0:
        return {"user_id": user_id, "recommended_videos": []}

    # ✅ Reshape input to match model expectations
    predictions = model.predict(video_ids.reshape(-1, 1))

    # ✅ Sort videos based on recommendation score
    recommended_videos = sorted(zip(video_ids, predictions.flatten()), key=lambda x: x[1], reverse=True)

    # ✅ Convert NumPy int to Python int for FastAPI JSON serialization
    top_videos = [int(video[0]) for video in recommended_videos[:5]]

    return {"user_id": user_id, "recommended_videos": top_videos}
