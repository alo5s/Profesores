# Instalar con pip install python-dotenv
from dotenv import load_dotenv  
import os

# Carga todo el contenido de .env en variables de entorno
load_dotenv()  

class Config(object):
    DEBUG = False   
    SECRET_KEY =  os.environ.get('SECRET_KET_FLASK')
    DB_TOKEN = os.environ.get("DB_TOKEN", "") 
    ENCRYPT_DB = True
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    
    TEMPLATE_FOLDER = "views/templates/"
    STATIC_FOLDER = "views/static/"

class ProductionConfig(Config):
    DEBUG = False
    SERVER_NAME = "0.0.0.0:8000"
class DevelopmentConfig(Config):
    DEBUG = True 
    SERVER_NAME = "localhost:8000"  
    