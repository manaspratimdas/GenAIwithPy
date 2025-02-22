import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

username = os.getenv('username')
password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')
mydatabase = os.getenv('mydatabase')

pg_uri = f"mysql+pymysql://root:{password}@localhost:3306/sakila"
engine = create_engine(pg_uri) 
db = SQLDatabase.from_uri(pg_uri)

def get_db_table_info():


   
    db_table_info = db.get_table_info()

    llm_transformer = LLMGraphTransformer(llm=llm)
    documents = [Document(page_content=db_table_info)]
    graph_documents_filtered = llm_transformer.convert_to_graph_documents(documents)

    nodes = f"Nodes:{graph_documents_filtered[0].nodes}"
    relationships = f"Relationships:{graph_documents_filtered[0].relationships}"

    concatenated_result = f"{nodes}\n{relationships}"

    return concatenated_result



