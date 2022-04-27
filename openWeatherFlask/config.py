class Config(object):
    TESTING = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    RATELIMIT_ENABLED = False

class TestingConfig(Config):
    TESTING = True
    RATELIMIT_ENABLED = False