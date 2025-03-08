# from fastapi import FastAPI
# from app.routes import recommendations
# from app.routes import data_fetch
# from app.routes import interactions

# app = FastAPI()

# app.include_router(recommendations.router, prefix="/api")
# app.include_router(data_fetch.router, prefix="/api")
# app.include_router(interactions.router, prefix="/api")
# # from fastapi import FastAPI
# # from app.routes import data_fetch  # Import the API route

# # app = FastAPI()

# # # ✅ Register the router with prefix "/api"
# # app.include_router(data_fetch.router, prefix="/api", tags=["Data Fetch"])
from fastapi import FastAPI
from app.routes import recommendations, data_fetch, interactions, recommendation_engine  # ✅ FIXED IMPORT

from app.database import engine, Base

# ✅ Ensure database tables are created
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ Include Routers
app.include_router(recommendations.router, prefix="/api", tags=["Recommendations"])
app.include_router(data_fetch.router, prefix="/api", tags=["Data Fetch"])
app.include_router(interactions.router, prefix="/api", tags=["User Interactions"])
app.include_router(recommendation_engine.router, prefix="/api", tags=["Recommendation Engine"])  # ✅ FIXED ROUTE

@app.get("/")
def home():
    return {"message": "Video Recommendation API is running"}
