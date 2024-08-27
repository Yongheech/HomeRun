from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    userid: str = ''
    passwd: str = ''
    dbname: str = 'user2024'
    dburl:  str = ''
    dbconn: str = f'sqlite:///app/{dbname}.db'

config = Settings()