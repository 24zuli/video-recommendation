from fastapi import FastAPI
from app.routes import recommendations, data_fetch, interactions, recommendation_engine  # ✅ FIXED IMPORT

from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(recommendations.router, prefix="/api", tags=["Recommendations"])
app.include_router(data_fetch.router, prefix="/api", tags=["Data Fetch"])
app.include_router(interactions.router, prefix="/api", tags=["User Interactions"])
app.include_router(recommendation_engine.router, prefix="/api", tags=["Recommendation Engine"])  # ✅ FIXED ROUTE

@app.get("/")
def home():
    return {"message": "Video Recommendation API is running"}
