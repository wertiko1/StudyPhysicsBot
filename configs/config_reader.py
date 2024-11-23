import os

from dotenv import load_dotenv


class Config:
    load_dotenv()
    TOKEN: str = os.getenv('TOKEN')
    MYSQL_URL: str = os.getenv('MYSQL_URL')
