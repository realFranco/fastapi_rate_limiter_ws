"""
To run the app:

cd app
uvicorn app:app --reload --port 8080
"""
import json
import asyncio
import time
from typing import Union

from fastapi import FastAPI, WebSocket

from route.car import car_router


app = FastAPI()

app.include_router(car_router, prefix="/car")
