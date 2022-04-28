import requests
import logging

from openWeatherFlask.models import City, CityTemp
from openWeatherFlask.alpha2_to_alpha3 import alpha2_to_alpha3
from openWeatherFlask.exceptions import CityNotFounded, InvalidAPIKey, RateLimit


def get_openWeatherData(api_key : str, city_name : str) -> type[CityTemp]:
    '''A function that make a request to the OpenWeather API and returns a CityTemp Object

        Parameters:
                    api_key (str): The api key provided by OpenWeather
                    city_name (str): The city name

            Returns:
                    cityTemp (CityTemp): An object define by models CityTemp
    
    '''

    query_string = {'q' : city_name, 'appid'  : api_key, 'units' : 'metric'}

    try :
        response = requests.get('https://api.openweathermap.org/data/2.5/weather', params = query_string)

    except requests.exceptions.RequestException as err:
        logging.exception(f"FAILED TO ESTABLISH THE CONNECTION to OpenWeatherAPI ERROR ({str(err)})")
        raise requests.exceptions.RequestException(f'FAILED TO ESTABLISH THE CONNECTION to OpenWeatherAPI ERROR ({str(err)})')

    if response.ok:

        return convert_openWeather_data_to_cityTemp(response.json())
    
    else:
        
        match response.status_code:
            case 404:
                logging.exception(f"City not founded in OpenWeatherAPI got HTTP code {response.status_code} return '{ response.text }'")
                raise CityNotFounded(response.json()['message'])
            case 401:
                logging.exception(f"INVALID API KEY ERROR the request to OpenWeatherAPI got HTTP code {response.status_code} return '{ response.text }'")
                raise InvalidAPIKey(response.json()['message'])
            case 429:
                logging.exception(f"RATE LIMIT ERROR the request to OpenWeatherAPI got HTTP code {response.status_code} return '{ response.text }'")
                raise RateLimit(response.json()['message'])
            case _:
                logging.exception(f"FAILED REQUEST to OpenWeatherAPI got HTTP code {response.status_code} return '{ response.text }'")
                raise ConnectionError('Internal error in OpenWeatherApi')

def convert_openWeather_data_to_cityTemp( response : dict ) -> type[CityTemp]:
    '''A function that get the dict response of the API OpenWeather and convert the data to CityTemp Model

        Parameters:
                    response (dict): The response of the api openWeather

            Returns:
                    cityTemp (CityTemp): An object define by models CityTemp
    
    '''
    city = City( 
                        name = response['name'], 
                        country = alpha2_to_alpha3[ response['sys']['country'] ]
                        )

    cityTemp_model = CityTemp(  id = response['id'], 
                                    min = response['main']['temp_min'], 
                                    max = response['main']['temp_max'], 
                                    avg = response['main']['temp'], 
                                    feels_like = response['main']['feels_like'], 
                                    city = city
                                    )
    
    return cityTemp_model

        




    