from os import environ
import logging
from flask import Flask, request, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from cachetools import TTLCache
import requests

from openWeatherFlask.util import get_openWeatherData
from openWeatherFlask.exceptions import CityNotFounded, InvalidAPIKey, RateLimit

OPEN_WEATHER_API_KEY = environ.get('OPEN_WEATHER_API_KEY')

if not OPEN_WEATHER_API_KEY:
    logging.exception("ENV variable OPEN_WEATHER_API_KEY not founded")
    exit(1)

CACHE_TTL = int(environ.get('CACHE_TTL', 300))
RATE_LIMIT = environ.get('RATE_LIMIT', 100)

DEFAULT_MAX_NUMBER = environ.get('DEFAULT_MAX_NUMBER', 5)
APPLICATION_MODE = environ.get('APPLICATION_MODE', 'PRD')

app = Flask(__name__)

match APPLICATION_MODE:
    case 'DEV':
        app.config.from_object('openWeatherFlask.config.DevelopmentConfig')
        pass
    case 'TEST':
        app.config.from_object('openWeatherFlask.config.TestingConfig')
        pass
    case 'PRD':
        app.config.from_object('openWeatherFlask.config.ProductionConfig')


cache = TTLCache(maxsize=200, ttl=CACHE_TTL)
limiter = Limiter(
    app,
    default_limits=[f'{DEFAULT_MAX_NUMBER} per minute'],
    key_func=get_remote_address
    )


@app.route('/<city_name>')
@app.route('/')
def hello(city_name = None):

    if not city_name:
        cache.expire()  # method that delete the cached data that is no longer valid

        list_data = []
        max_itens = min( int( request.args.get('max', DEFAULT_MAX_NUMBER ) ), cache.currsize ) # First is checked if the the GET param 'max' is being send, if not a DEFAULT_MAX_NUMBER defined by env variables is used istead, and finaly is compare that number with the lenght of the cache and get the min value between the two
                  
        for key in cache: 
            list_data.append(cache[key].dict())

        list_data.reverse()
        
        return { 'cities_cached' : list_data[:max_itens]}


    city_name = city_name.strip().title() # Format the city string name
    if city_name not in cache:
        try:
            cache[city_name] = get_openWeatherData(api_key = OPEN_WEATHER_API_KEY, city_name = city_name)
        except requests.exceptions.RequestException as err:
            return {'code': 500, 'message' : str(err)}, 500
        except CityNotFounded as city_err:
            return {'code': 404, 'message' : str(city_err)}, 404
        except InvalidAPIKey as err:
            return {'code': 401, 'message' : str(err)}, 401
        except RateLimit as err:
            return {'code': 429, 'message' : str(err)}, 429
        except ConnectionError as err:
            return {'code': 500, 'message' : str(err)}, 500
        
    
    return cache[city_name].dict()

@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
            {'error': "Rate limit reached (%s)" % e.description}, 429
    )
