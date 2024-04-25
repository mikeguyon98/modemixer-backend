# app/main.py
from fastapi import FastAPI
from app.config import global_init
from app.routes.routes import router

global_init()  # Initialize the database connection

app = FastAPI()
app.include_router(router)