from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import engine, SessionLocal, Base
from routers import dashboard, login
from sqlalchemy.orm import Session

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup():
    # Initialize database session
    SessionLocal()

@app.on_event("shutdown")
def shutdown():
    # Close database session
    SessionLocal().close()

app.include_router(login.router)
app.include_router(dashboard.router)



