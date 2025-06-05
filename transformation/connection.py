import os
from sqlalchemy import create_engine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'covid_data.db')


engine = create_engine(f'sqlite:///{DB_PATH}')

