from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, StrictFloat, StrictStr, HttpUrl
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
import time

app = FastAPI()

# In-memory database to store id and extracted_insight(For Task 3 in-memory storage)
reports_db = []

# Used model to check Strict types,
class Location(BaseModel):
    latitude: StrictFloat
    longitude: StrictFloat

class Observation(BaseModel):
    observation_id: StrictStr
    user_id: StrictStr
    text_observation: StrictStr
    photo_url: HttpUrl
    location: Location

# Custom validation, By default fastapi send 422 status code but we need 400
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("validation failed")
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={
            "message": "Bad Request. Validation failed.",
            "errors": exc.errors()
        },
    )

# Simulated LLM Interaction:
def mock_llm_extract_info(text_data):
    try:
        print("mock_llm_extract_info called")
        time.sleep(1)
        print("Success: Mock LLM: Insight extracted")
        return "Mock LLM: Insight extracted."
    except Exception as e:
        print(f"Error in mock_llm_extract_info: {e}")
        return None

# API Endpoint (POST /submit_observation):
@app.post("/observation")
def submit_observation(observation: Observation):
    try:
        print("Observation received:")
        extracted_insight = mock_llm_extract_info(observation.text_observation)
        if not extracted_insight:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to extract insight.")
        
        # Add record in reports(WE can update record with same observation_id)
        reports_db.append({
            "id": observation.observation_id,
            "extracted_insight": extracted_insight
        })
        print("observation processed")
        return {
            "message": "received",
            "id": observation.observation_id
        }
    except HTTPException:
        # Re-raise HTTPExceptions to be handled by FastAPI
        raise
    except Exception as e:
        print(f"Unexpected error in submit_observation: {e}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

@app.get("/reports")
def reports():
    try:
        if not reports_db:
            return {
                "message": "No reports available.",
                "reports": []
            }
        return {
            "message": "Report fetched successfully",
            "reports": reports_db
        }
    except Exception as e:
        print(f"Error fetching reports: {e}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch reports.")
