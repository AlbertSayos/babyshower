import os
from dotenv import load_dotenv

env_path = '.env'

load_dotenv(dotenv_path=env_path)

stringConn = os.getenv('DB_INV')