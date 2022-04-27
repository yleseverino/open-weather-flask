from os import environ
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import datetime
from cachetools import TTLCache
import config


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


cache = TTLCache(maxsize=10, ttl=CACHE_TTL)
limiter = Limiter(
    app,
    default_limits=[f'{DEFAULT_MAX_NUMBER} per minute'],
    key_func=get_remote_address
    )


@app.route('/<city_name>')
@app.route('/')
def hello(city_name = None):
    if not city_name:
        print(cache)
        return 'tess'
    cache[city_name] = 25
    return f'100'