from fastapi import FastAPI

from app.routers import auth, points


app = FastAPI()

app.include_router(auth.router)
app.include_router(points.router)
