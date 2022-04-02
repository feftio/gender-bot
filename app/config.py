import os

TOKEN: str = os.environ.get('TOKEN', '')
DB_PATH: str = os.environ.get('DB_PATH', 'sqlite.db')
PROJECT_PATH: str = os.getcwd()
