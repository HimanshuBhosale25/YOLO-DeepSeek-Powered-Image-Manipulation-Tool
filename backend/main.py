from fastapi import FastAPI
from api import image_api
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv() 

app = FastAPI()

origins = [
  "http://localhost:5173",  
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(image_api.router)


@app.get("/test")
async def test():
  return {"message": "FastAPI is working!"}