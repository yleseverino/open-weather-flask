from os import environ
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import datetime
from cachetools import TTLCache

from models import City, CityTemp
from util import get_openWeatherData

OPEN_WEATHER_API_KEY = environ.get('OPEN_WEATHER_API_KEY')

if not OPEN_WEATHER_API_KEY:
    print('ENV variable OPEN_WEATHER_API_KEY not founded')
    exit(1)

CACHE_TTL = int(environ.get('CACHE_TTL', 300))
DEFAULT_MAX_NUMBER = environ.get('DEFAULT_MAX_NUMBER', 5)
APPLICATION_MODE = environ.get('APPLICATION_MODE', 'PRD')

app = Flask(__name__)

match APPLICATION_MODE:
    case 'DEV':
        app.config.from_object('config.DevelopmentConfig')
        pass
    case 'TEST':
        app.config.from_object('config.TestingConfig')
        pass
    case 'PRD':
        app.config.from_object('config.ProductionConfig')


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
        return 'tess'

    city_name = city_name.strip().capitalize() # Format the city string name
    if city_name not in cache:
        cache[city_name] = get_openWeatherData(api_key = OPEN_WEATHER_API_KEY, city_name = city_name)
    
    return cache[city_name].json()
