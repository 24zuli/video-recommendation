import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sqlalchemy.orm import Session
from sklearn.model_selection import train_test_split
from app.database import SessionLocal
from app.models import UserInteraction

MODEL_PATH = "app/recommendation/recommendation_model.keras"  

INTERACTION_WEIGHTS = {
    "view": 0.3,     
    "like": 1.0,      
    "inspired": 0.8,   
    "rated": 0.9      
}

def train_recommendation_model():
    db: Session = SessionLocal()

    try:
      
        interactions = db.query(UserInteraction).all()

        if not interactions:
            print("No interactions found. Cannot train model.")
            return


        user_ids = np.array([interaction.user_id for interaction in interactions])
        video_ids = np.array([interaction.video_id for interaction in interactions])

        
        labels = np.array([
            INTERACTION_WEIGHTS.get(interaction.interaction_type, 0)  
            for interaction in interactions
        ])
        
        unique_videos = np.unique(video_ids)
        video_to_index = {video: idx for idx, video in enumerate(unique_videos)}
        video_ids = np.array([video_to_index[v] for v in video_ids])

        num_videos = len(unique_videos) 

        X_train, X_val, y_train, y_val = train_test_split(video_ids, labels, test_size=0.2, random_state=42)

        model = keras.Sequential([
            layers.Embedding(input_dim=num_videos, output_dim=32, input_length=1),
            layers.Flatten(),
            layers.Dense(64, activation="relu"),
            layers.Dropout(0.3),
            layers.Dense(32, activation="relu"),
            layers.Dense(1, activation="sigmoid") 
        ])

        model.compile(optimizer="adam", loss="mse", metrics=["mae"])

        early_stopping = keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=3,
            restore_best_weights=True
        )

        print("Training started...")
        history = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=20,  
            batch_size=8,
            verbose=1,
            callbacks=[early_stopping]
        )

        model.save(MODEL_PATH)
        print(f"Model trained and saved at {MODEL_PATH}")

    finally:
        db.close()  


if __name__ == "__main__":
    train_recommendation_model()

