# import numpy as np
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# from sqlalchemy.orm import Session
# from app.database import SessionLocal
# from app.models import UserInteraction

# MODEL_PATH = "app/recommendation/recommendation_model.h5"

# def train_recommendation_model():
#     db: Session = SessionLocal()
    
#     # Fetch user interactions
#     interactions = db.query(UserInteraction).all()
    
#     if not interactions:
#         print("No interactions found. Cannot train model.")
#         return

#     # Prepare training data
#     user_ids = np.array([interaction.user_id for interaction in interactions])
#     video_ids = np.array([interaction.video_id for interaction in interactions])
#     labels = np.array([1 if interaction.interaction_type == "like" else 0 for interaction in interactions])

#     # Define model
#     model = keras.Sequential([
#         layers.Embedding(input_dim=1000, output_dim=32, input_length=1),  # Adjust input_dim based on data
#         layers.Flatten(),
#         layers.Dense(64, activation="relu"),
#         layers.Dropout(0.3),
#         layers.Dense(32, activation="relu"),
#         layers.Dense(1, activation="sigmoid")
#     ])

#     model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    
#     # Train model
#     print("Training started...")
#     model.fit(video_ids, labels, epochs=10, batch_size=8, verbose=1)

#     # Save model
#     model.save(MODEL_PATH)
#     print(f"Model trained and saved at {MODEL_PATH}")

# if __name__ == "__main__":
#     train_recommendation_model()


# import numpy as np
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# from sqlalchemy.orm import Session
# from sklearn.model_selection import train_test_split
# from app.database import SessionLocal
# from app.models import UserInteraction

# MODEL_PATH = "app/recommendation/recommendation_model.keras"  # Changed to modern format


# def train_recommendation_model():
#     db: Session = SessionLocal()

#     try:
#         # Fetch user interactions
#         interactions = db.query(UserInteraction).all()

#         if not interactions:
#             print("No interactions found. Cannot train model.")
#             return

#         # Prepare training data
#         user_ids = np.array([interaction.user_id for interaction in interactions])
#         video_ids = np.array([interaction.video_id for interaction in interactions])
#         labels = np.array([1 if interaction.interaction_type == "like" else 0 for interaction in interactions])

#         # Normalize video IDs to be used in Embedding layer
#         unique_videos = np.unique(video_ids)
#         video_to_index = {video: idx for idx, video in enumerate(unique_videos)}
#         video_ids = np.array([video_to_index[v] for v in video_ids])

#         num_videos = len(unique_videos)  # Dynamically set input_dim

#         # Split dataset into training & validation
#         X_train, X_val, y_train, y_val = train_test_split(video_ids, labels, test_size=0.2, random_state=42)

#         # Define model
#         model = keras.Sequential([
#             layers.Embedding(input_dim=num_videos, output_dim=32, input_length=1),
#             layers.Flatten(),
#             layers.Dense(64, activation="relu"),
#             layers.Dropout(0.3),
#             layers.Dense(32, activation="relu"),
#             layers.Dense(1, activation="sigmoid")
#         ])

#         model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

#         # Add EarlyStopping
#         early_stopping = keras.callbacks.EarlyStopping(
#             monitor="val_loss",
#             patience=3,
#             restore_best_weights=True
#         )

#         # Train model with validation
#         print("Training started...")
#         history = model.fit(
#             X_train, y_train,
#             validation_data=(X_val, y_val),
#             epochs=20,  # Increased but will stop early if needed
#             batch_size=8,
#             verbose=1,
#             callbacks=[early_stopping]
#         )

#         # Save model in modern Keras format
#         model.save(MODEL_PATH)
#         print(f"Model trained and saved at {MODEL_PATH}")

#     finally:
#         db.close()  # Ensure DB session is closed


# if __name__ == "__main__":
#     train_recommendation_model()

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sqlalchemy.orm import Session
from sklearn.model_selection import train_test_split
from app.database import SessionLocal
from app.models import UserInteraction

MODEL_PATH = "app/recommendation/recommendation_model.keras"  # Changed to modern format

# ✅ Assign weights to different interaction types
INTERACTION_WEIGHTS = {
    "view": 0.3,       # Low weight since it doesn't mean preference
    "like": 1.0,       # Strongest weight
    "inspired": 0.8,   # Shows strong engagement
    "rated": 0.9       # Almost as strong as like
}

def train_recommendation_model():
    db: Session = SessionLocal()

    try:
        # Fetch user interactions
        interactions = db.query(UserInteraction).all()

        if not interactions:
            print("No interactions found. Cannot train model.")
            return

        # Prepare training data
        user_ids = np.array([interaction.user_id for interaction in interactions])
        video_ids = np.array([interaction.video_id for interaction in interactions])

        # ✅ Assign weighted labels based on interaction type
        labels = np.array([
            INTERACTION_WEIGHTS.get(interaction.interaction_type, 0)  # Default weight is 0
            for interaction in interactions
        ])

        # Normalize video IDs to be used in Embedding layer
        unique_videos = np.unique(video_ids)
        video_to_index = {video: idx for idx, video in enumerate(unique_videos)}
        video_ids = np.array([video_to_index[v] for v in video_ids])

        num_videos = len(unique_videos)  # Dynamically set input_dim

        # Split dataset into training & validation
        X_train, X_val, y_train, y_val = train_test_split(video_ids, labels, test_size=0.2, random_state=42)

        # Define model
        model = keras.Sequential([
            layers.Embedding(input_dim=num_videos, output_dim=32, input_length=1),
            layers.Flatten(),
            layers.Dense(64, activation="relu"),
            layers.Dropout(0.3),
            layers.Dense(32, activation="relu"),
            layers.Dense(1, activation="sigmoid")  # ❌ Change to 'linear' for continuous predictions
        ])

        # ✅ Change loss to 'mse' since labels are now continuous
        model.compile(optimizer="adam", loss="mse", metrics=["mae"])

        # Add EarlyStopping
        early_stopping = keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=3,
            restore_best_weights=True
        )

        # Train model with validation
        print("Training started...")
        history = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=20,  # Increased but will stop early if needed
            batch_size=8,
            verbose=1,
            callbacks=[early_stopping]
        )

        # Save model in modern Keras format
        model.save(MODEL_PATH)
        print(f"Model trained and saved at {MODEL_PATH}")

    finally:
        db.close()  # Ensure DB session is closed


if __name__ == "__main__":
    train_recommendation_model()

