from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from poibot import poidetails
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="POI Curator API")

# CORS - Very important for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PoiQuery(BaseModel):
    query: str

# Health Check Route
@app.get("/")
async def root():
    return {"status": "alive", "message": "POI Curator API is running"}

@app.post("/curatepoi")
async def fetchpoi(poiquery: PoiQuery):
    try:
        logger.info(f"Received query: {poiquery.query}")
        
        if not poiquery.query or len(poiquery.query.strip()) < 3:
            return {"error": "Query too short"}

        result = poidetails(poiquery.query.strip())
        
        logger.info("Successfully processed POI")
        return result

    except Exception as e:
        logger.error(f"Error processing POI: {str(e)}")
        return {
            "error": "Failed to process POI",
            "detail": str(e)
        }