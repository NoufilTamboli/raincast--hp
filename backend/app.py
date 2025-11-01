# backend/app.py

from fastapi import FastAPI
from backend.database import engine, Base
from backend.routes import router  # ✅ Import your routes from routes.py

# Initialize FastAPI app
app = FastAPI(title="RainCast HP API", version="1.0")

# ✅ Include all routes from routes.py
app.include_router(router)

# ✅ Create database tables on startup
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
