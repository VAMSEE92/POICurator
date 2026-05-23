from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from poibot import poidetails
import os


app = FastAPI()
# Allow Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class PoiQuery(BaseModel):
    query:str

@app.post("/curatepoi")
def fetchpoi(poiquery:PoiQuery):
    poi = poiquery.query
    return poidetails(poi)

