from pydantic import BaseModel, ValidationError, validator
from datetime import datetime
from alpha2_to_alpha3 import alpha2_to_alpha3


class City(BaseModel):
    id: int
    name: str
    country: str

    @validator('country')
    def country_must_be_alpha_3_format(cls, v):
        if v not in alpha2_to_alpha3.values():
            raise ValueError('country must be alpha 3 format (ISO 3166-1)')
        return v

class CityTemp(BaseModel):
    id: int
    min: float
    max: float
    avg: float
    feels_like: float
    city: City
    timestamp: datetime = datetime.now()