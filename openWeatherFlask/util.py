import requests
from models import City, CityTemp
from alpha2_to_alpha3 import alpha2_to_alpha3


def get_openWeatherData(api_key : str, city_name : str) -> type[CityTemp]:
    '''A function that make a request to the OpenWeather API and returns a CityTemp Object

        Parameters:
                    api_key (str): The api key provided by OpenWeather
                    city_name (str): The city name

            Returns:
                    cityTemp (CityTemp): An object define by models CityTemp
    
    '''

    query_string = {'q' : city_name, 'appid'  : api_key, 'units' : 'metric'}
    r = requests.get('https://api.openweathermap.org/data/2.5/weather', params = query_string)

    res = r.json()
    city = City(id = res['sys']['id'], name = city_name, country = alpha2_to_alpha3[ res['sys']['country'] ])
    cityTemp_model = CityTemp(id = res['id'], min = res['main']['temp_min'], max = res['main']['temp_max'], avg = res['main']['temp'], feels_like = res['main']['feels_like'], city = city)
    return cityTemp_model



    