from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)

    interactions = relationship("UserInteraction", back_populates="user")


class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    video_metadata = Column(JSON, nullable=True) 
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    view_count = Column(Integer, nullable=True) 
    upvote_count = Column(Integer, nullable=True)
    comment_count = Column(Integer, nullable=True)
    video_link = Column(String, nullable=True)
    thumbnail_url = Column(String, nullable=True)

    interactions = relationship("UserInteraction", back_populates="video")


class UserInteraction(Base):
    __tablename__ = 'user_interactions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    video_id = Column(Integer, ForeignKey('videos.id', ondelete="CASCADE"), nullable=False)
    interaction_type = Column(String, nullable=False)  # e.g., "like", "view", "inspire"
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="interactions")
    video = relationship("Video", back_populates="interactions")
