from pydantic import BaseModel
from datetime import datetime


class City(BaseModel):
    id: int
    name:str
    country:str

class CityTemp(BaseModel):
    id: int
    min: float
    max: float
    avg: float
    feels_like: float
    city: City
    timestamp: datetime = datetime.now()