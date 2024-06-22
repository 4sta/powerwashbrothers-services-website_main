import os
from sqlalchemy import create_engine


username = 'root'
password = 'Strongpass!'
database = 'website'
host = '35.234.97.3'
port = '3306' 


ssl_ca = os.getenv('SSL_CA_PATH')     
ssl_cert = os.getenv('SSL_CERT_PATH')  
ssl_key = os.getenv('SSL_KEY_PATH')   


if not all([ssl_ca, ssl_cert, ssl_key]):
    print("Missing SSL configurations in environment variables")
    exit()


connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?ssl_ca={ssl_ca}&ssl_cert={ssl_cert}&ssl_key={ssl_key}"
engine = create_engine(connection_string)


try:
    with engine.connect() as connection:
        print("Successfully connected to the database!")
except Exception as e:
    print(f"Connection Error: {e}")