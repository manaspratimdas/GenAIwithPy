# database_utils.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, MetaData, inspect


load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

username = os.getenv('username')
password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')
mydatabase = os.getenv('mydatabase')

pg_uri = f"mysql+pymysql://root:{password}@localhost:3306/sakila"
engine = create_engine(pg_uri) 

db = SQLDatabase(engine)

metadata = MetaData()
metadata.reflect(bind=engine)

inspector = inspect(engine)

def list_database_tables():


    # Get list of tables
    tables = inspector.get_table_names()
   
    return tables
