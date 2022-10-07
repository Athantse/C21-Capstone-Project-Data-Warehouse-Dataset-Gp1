from dotenv import load_dotenv

import os

class Config:
    def __init__(self):
        load_dotenv()
        self.POSTGRES_DB=os.getenv('POSTGRES_DB')
        self.POSTGRES_DW=os.getenv('POSTGRES_DW')
        self.POSTGRES_USER=os.getenv('POSTGRES_USER')
        self.POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
        self.POSTGRES_HOST=os.getenv('POSTGRES_HOST')
        self.AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY')
        self.AWS_SECRET_KEY=os.getenv('AWS_SECRET_KEY')
        self.SPARK_MASTER=os.getenv('SPARK_MASTER')
        self.RDS_POSTGRES_HOST=os.getenv('RDS_POSTGRES_HOST')
        self.RDS_POSTGRES_DB=os.getenv('RDS_POSTGRES_DB')
        self.RDS_POSTGRES_USER=os.getenv('RDS_POSTGRES_USER')
        self.RDS_POSTGRES_PASSWORD=os.getenv('RDS_POSTGRES_PASSWORD')

