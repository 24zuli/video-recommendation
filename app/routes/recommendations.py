import requests
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
import os

router = APIRouter()

FLIC_TOKEN = os.getenv("FLIC_TOKEN")
HEADERS = {"Flic-Token": FLIC_TOKEN}
API_BASE_URL = os.getenv("API_BASE_URL")

@router.get("/feed")
def get_personalized_feed(username: str, db: Session = Depends(get_db)):
    if not FLIC_TOKEN:
        return {"error": "FLIC_TOKEN not found. Please set it in .env file."}

    response = requests.get(f"{API_BASE_URL}/posts/view", headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data from external API", "status": response.status_code}
