from fastapi import FastAPI, Request
from pydantic import BaseModel, StrictFloat, StrictStr
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

app = FastAPI()

class Location(BaseModel):
    latitude: StrictFloat
    longitude: StrictFloat

class Observation(BaseModel):
    observation_id: StrictStr
    user_id: StrictStr
    text_observation: StrictStr
    photo_url: StrictStr
    location: Location

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={
            "message": "Bad Request. Validation failed.",
            "errors": exc.errors()
        },
    )

@app.post("/observation")
def submit_observation(observation:Observation):
    return {
        "message": "received",
        "id": observation.observation_id
    }

