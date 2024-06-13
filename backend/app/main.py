from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from app.routers import auth, points
from app import custom_logging

LOGGER = custom_logging.get_logger(__name__)


LOGGER.info("Setting up the fastapi app")
# Create FastAPI app
app: FastAPI = FastAPI()

# Set up CORS origins to allow requests from the frontend
origins: List[str] = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(points.router)

if __name__ == "__main__":
    LOGGER.info("Starting the application")