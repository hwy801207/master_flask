class Config:
    pass

class PrdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://hwy:hwy@127.0.0.1/forums"
