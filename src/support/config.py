# =========================================================================
# 
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
# 
# Configuration
# 
# =========================================================================

# Returns a configuration object containing relevant environment parameters.
# Base config class with universal parameters
# Child classes with environment specific parameters which can be adjusted for deployment, local testing etc.


import os
from logging import Logger
import boto3
import json

# Parent class for any variables which are independent of operating system:
class Config:

    EXAMPLE_GENERIC_VARIABLE = True

# AWS config should also work for local Docker testing:
class AWSConfig(Config):
    #TODO: prevent hard code sensitive data
    def __init__(self):

        self.FRONTEND_HOST = "0.0.0.0" 
        self.FRONTEND_PORT = 80
        self.TEMPLATES_DIR = "../app/templates"
        self.BASE_HREF = "ec2-3-26-255-162.ap-southeast-2.compute.amazonaws.com"

        aws_region="ap-southeast-2"
        db_secret_name=os.environ.get('DB_SECRET_NAME')
        # session = boto3.session.Session()
        # client = session.client(
        #     service_name='secretsmanager',
        #     region_name=aws_region
        # )
        # db_response = client.get_secret_value(SecretId=db_secret_name)
        # db_details = json.loads(db_response['SecretString'])
        
        self.DB_DRIVERNAME="postgresql+psycopg2"
        self.DB_USERNAME="postgres"
        self.DB_HOST="database-1.cpmp7xm6rr99.ap-southeast-2.rds.amazonaws.com"
        self.DB_PORT="5432"
        self.DB_DATABASE="database-1"
        self.DB_PASSWORD=input("Enter DB password:")
        # self.SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
        # self.ALGORITHM = "HS256"
        # self.ACCESS_TOKEN_EXPIRE_MINUTES = 30

        

# For windows users. Will need to set up postgres locally, and create a new db with details per below:
class WindowsConfig(Config):

    def __init__(self):

        self.FRONTEND_HOST = "localhost"
        self.FRONTEND_PORT = 8000
        self.TEMPLATES_DIR = os.getcwd() + "/src/templates/" 
        self.BASE_HREF = "http://localhost:8000"
        self.DB_DRIVERNAME="postgresql+psycopg2"
        self.DB_USERNAME="postgres"
        self.DB_HOST="localhost"
        self.DB_PORT="5432"
        self.DB_DATABASE="vr1_db1"
        self.DB_PASSWORD=input("Enter DB password:")
        self.SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30


# For Apple users. Will need to set up postgres locally, and create a new db with details per below (or as amended):
# (Apple currently identical to Windows config. Apple users can amend later if required)
class AppleConfig(Config):

    def __init__(self):

        self.FRONTEND_HOST = "localhost"
        self.FRONTEND_PORT = 8000
        self.TEMPLATES_DIR = os.getcwd() + "/src/templates/" 
        self.BASE_HREF = "http://localhost:8000"
        self.DB_DRIVERNAME="postgresql+psycopg2"
        self.DB_USERNAME="postgres"
        self.DB_HOST="localhost"
        self.DB_PORT="5432"
        self.DB_DATABASE="vr1_db1"
        self.DB_PASSWORD=input("Enter DB password:")
        self.SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_config(log: Logger):
    
    import platform
    plt = platform.system()
    if plt == "Linux":
        log.info("AWS / Docker Environment Selected.")
        return AWSConfig()
    elif plt == "Darwin":
        log.info("Apple Environment Selected.")
        return AppleConfig()
    else:
        log.info("Windows Environment Selected.")
        return WindowsConfig() 

    
