from fastapi import FastAPI
# from routers import auth, points
from app.routers import auth, points
# from database import engine, Base
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(points.router)
