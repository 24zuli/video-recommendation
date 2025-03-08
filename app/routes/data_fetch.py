from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.fetch_data import fetch_and_store_videos

router = APIRouter()

@router.get("/fetch-videos") 
def fetch_videos(db: Session = Depends(get_db)):
    """
    Fetch videos from the external API and store them in the database.
    """
    return fetch_and_store_videos(db)
