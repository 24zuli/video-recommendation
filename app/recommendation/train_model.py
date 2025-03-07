import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import UserInteraction, Video

MODEL_PATH = "app/recommendation/recommendation_model.h5"

def train_recommendation_model():
    db: Session = SessionLocal()
    
    # Fetch user interactions
    interactions = db.query(UserInteraction).all()
    
    if not interactions:
        print("No interactions found. Cannot train model.")
        return

    # Prepare training data
    user_ids = np.array([interaction.user_id for interaction in interactions])
    video_ids = np.array([interaction.video_id for interaction in interactions])
    labels = np.array([1 if interaction.interaction_type == "like" else 0 for interaction in interactions])

    # Define model
    model = keras.Sequential([
        layers.Embedding(input_dim=1000, output_dim=32, input_length=1),  # Adjust input_dim based on data
        layers.Flatten(),
        layers.Dense(64, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(32, activation="relu"),
        layers.Dense(1, activation="sigmoid")
    ])

    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    
    # Train model
    model.fit(video_ids, labels, epochs=10, batch_size=16)

    # Save model
    model.save(MODEL_PATH)
    print("Model trained and saved.")

if __name__ == "__main__":
    train_recommendation_model()
