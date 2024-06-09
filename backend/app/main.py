from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, points


app = FastAPI()

origins = [
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
