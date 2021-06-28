import pyodbc 

DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
CORS_HEADERS = 'Content-Type'
SECRET_KEY = "asdjkgasd$#43"
SQLALCHEMY_ECHO = False
UPLOAD_FOLDER = 'app\\static\\files'
GEVENT_SUPPORT=True

SQLALCHEMY_DATABASE_URI = "sqlite:///storage.db"
#SQLALCHEMY_DATABASE_URI = "postgres://mfypepyiwdijkp:c27ded53bdc3de96e9bfec2250308ca4e90ee9c6838f9f448a5c1e5b2739ffd4@ec2-54-145-249-177.compute-1.amazonaws.com:5432/deu9bj7oqoeodq"

SERVER = "rpamonitor.database.windows.net" 
DB = "DB_RPA_Monitor" 
USER = "rpa_admin" 
PWD = "rP@ev0x1" 

drivers = [item for item in pyodbc.drivers()] 
driverH = drivers[-1]
driver = "SQL+Server"
print("driver:{}".format(driver)) 

SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{USER}:{PWD}@{SERVER}/{DB}?driver={driverH}"