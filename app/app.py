"""
To run the app:

cd app
uvicorn app:app --reload --port 8080
"""
from fastapi import FastAPI

from route.car import car_router


app = FastAPI()

app.include_router(car_router, prefix="/car")
