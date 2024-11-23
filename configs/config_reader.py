import os

from dotenv import load_dotenv


class Config:
    load_dotenv()
    TOKEN: str = os.getenv('TOKEN')
    SQL_URL: str = os.getenv('SQL_URL')
