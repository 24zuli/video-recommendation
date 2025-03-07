# import requests
# from sqlalchemy.orm import Session
# from app.models import Video

# # ✅ Define the API endpoint
# VIDEO_API_URL = "http://127.0.0.1:8000/api/feed?username=test_user"  # Replace with actual API

# def get_videos_from_api():
#     """
#     Fetches video data from the API.
#     Returns a dictionary containing video data.
#     """
#     try:
#         response = requests.get(VIDEO_API_URL)
#         response.raise_for_status()  # Raise an error for bad status codes
#         return response.json()  # ✅ Ensure this returns a dictionary
#     except requests.RequestException as e:
#         print(f"Error fetching videos: {e}")
#         return {"posts": []}  # ✅ Return empty posts if API fails

# def fetch_and_store_videos(db: Session):
#     """
#     Fetches videos from the API and stores them in the database.
#     """
#     api_response = get_videos_from_api()  # ✅ Fetch API data
    
#     if not api_response or "posts" not in api_response:
#         print("Error: Invalid API response format.")
#         return {"message": "Invalid API response"}

#     for video_data in api_response["posts"]:  # ✅ Ensure we are iterating correctly
#         existing_video = db.query(Video).filter(Video.id == video_data["id"]).first()
        
#         if not existing_video:
#             new_video = Video(
#                 id=video_data["id"],
#                 title=video_data.get("title", "Untitled"),  # Default if missing
#                 category=video_data["category"]["name"],  # Extract category
#                 video_metadata=video_data,  # Store full JSON metadata
#                 view_count=video_data.get("view_count", 0),
#                 upvote_count=video_data.get("upvote_count", 0),
#                 comment_count=video_data.get("comment_count", 0),
#                 video_link=video_data.get("video_link", ""),
#                 thumbnail_url=video_data.get("thumbnail_url", ""),
#             )
#             db.add(new_video)

#     db.commit()
#     return {"message": "Videos stored successfully"}

import requests
from sqlalchemy.orm import Session
from app.models import Video, User

# ✅ Define the API endpoint
VIDEO_API_URL = "http://127.0.0.1:8000/api/feed?username=test_user"

def get_videos_from_api():
    """
    Fetches video data from the API.
    Returns a dictionary containing video data.
    """
    try:
        response = requests.get(VIDEO_API_URL)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()  # ✅ Ensure this returns a dictionary
    except requests.RequestException as e:
        print(f"Error fetching videos: {e}")
        return {"posts": []}  # ✅ Return empty posts if API fails

def fetch_and_store_videos(db: Session):
    """
    Fetches videos from the API and stores them in the database.
    """
    api_response = get_videos_from_api()  # ✅ Fetch API data
    
    if not api_response or "posts" not in api_response:
        print("Error: Invalid API response format.")
        return {"message": "Invalid API response"}

    for video_data in api_response["posts"]:  # ✅ Ensure we are iterating correctly
        # ✅ Store User if not already in DB
        user = db.query(User).filter(User.username == video_data["username"]).first()
        if not user:
            new_user = User(username=video_data["username"])
            db.add(new_user)
            db.commit()  # Commit to get ID immediately
            db.refresh(new_user)
            user_id = new_user.id
        else:
            user_id = user.id

        # ✅ Store Video if not already in DB
        existing_video = db.query(Video).filter(Video.id == video_data["id"]).first()
        if not existing_video:
            new_video = Video(
                id=video_data["id"],
                title=video_data.get("title", "Untitled"),
                category=video_data["category"]["name"],
                video_metadata=video_data,
            )
            db.add(new_video)

    db.commit()
    return {"message": "Users and videos stored successfully"}
