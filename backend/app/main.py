from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from app.routers import auth, points
from app import custom_logging

LOGGER = custom_logging.get_logger(__name__)


LOGGER.info("Setting up the fastapi app")
# Create FastAPI app
app: FastAPI = FastAPI(
    title="Geospatial Point Management API",
    description="API to create, read, update, and delete geospatial points.",
    responses={
        200: {"description": "Success"},
        201: {"description": "Created"},
        204: {"description": "No Content"},
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not Found"},
        405: {"description": "Method Not Allowed"},
        429: {"description": "Too Many Requests"},
        500: {"description": "Internal Server Error"},
        503: {"description": "Service Unavailable"},
        422: {"description": "Validation Error"},
    },
)

# Set up CORS origins to allow requests from the frontend
origins: List[str] = [
    "http://localhost:3000",
]

try:
    LOGGER.info("Adding CORS middleware to the app")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
except Exception as e:
    LOGGER.error(f"Error adding CORS middleware: {e}")

# Include routers
try:
    LOGGER.info("Including routers to the app")
    app.include_router(auth.router)
    app.include_router(points.router)
except Exception as e:
    LOGGER.error(f"Error including routers: {e}")

if __name__ == "__main__":
    LOGGER.info("Starting the application")