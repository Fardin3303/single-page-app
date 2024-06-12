from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from app.routers import auth, points
from app.custom_logging import LOGGER


# Create FastAPI app
app: FastAPI = FastAPI()

# Set up CORS origins
origins: List[str] = [
    "http://host.docker.internal:3000",
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
    LOGGER.info("Starting the application.")