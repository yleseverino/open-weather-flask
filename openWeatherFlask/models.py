from pydantic import BaseModel


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


a = City(id= 1, name = 'uberaba', country = 'BR')
b = CityTemp(id = 1, min = 20.05, max = 45.12, avg = 52.31, feels_like = 25.25, city = a)