from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Location(BaseModel):
    latitude: float
    longitude: float

class Observation(BaseModel):
    observation_id: str
    user_id: str
    text_observation: str
    photo_url: str
    location: Location


@app.post("/observation")
def submit_observation(observation:Observation):
    return {
        "message": "received",
        "id": observation.observation_id
    }