# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.collections_routes import router as collection_router
from app.routes.items_routes import router as item_router
from app.db import global_init
import uvicorn
import os

global_init()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Starting app at port: ", os.getenv("PORT"))

app.include_router(item_router)
app.include_router(collection_router)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)