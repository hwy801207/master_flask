class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=False
    SECRET_KEY="youSeCret%34#"

class PrdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://hwy:hwy@127.0.0.1/forums"
