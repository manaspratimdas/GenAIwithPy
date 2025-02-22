import os
import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_community.agent_toolkits.sql.toolkit import  SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import pymysql  # If using PyMySQL
# clearclarcfrom langchain.chains import SQLDatabaseSequentialChain
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain


import pandas as pd


load_dotenv()

llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

output_parser =StrOutputParser()

st.title("SQL DB Agent Implementation using Langchain")

username = os.getenv('username')
password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')
mydatabase = os.getenv('mydatabase')


pg_uri = f"mysql+pymysql://root:{password}@localhost:3306/sakila"
db = SQLDatabase.from_uri(pg_uri)



PROMPT = """ 
Given an input question, first create a syntactically correct mysql query to run,  
then look at the results of the query and return the answer.  
The question: {question}
"""

# db_chain = SQLDatabaseSequentialChain(llm=llm, database=db, verbose=True, top_k=3)
# db_chain = SQLDatabaseChain.from_llm(llm, db)
# question = "List the top 5 actors" 
# # use db_chain.run(question) instead if you don't have a prompt
# result=db_chain.invoke(
#     PROMPT.format(question=question)
#     ) 

# print(result)

SQL_PREFIX = """You are a MySQL expert. Given an input question, first create a syntactically correct SQLite query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use date('now') function to get the current date, if the question involves "today".
"""

# SQL_SUFFIX=""" 
# Preset the answer in human natural language. 
# """

Question=st.text_input("Ask your question here: ")



toolkit=SQLDatabaseToolkit(
    db=db,
    llm=llm
    )

sql_agent=create_sql_agent(
    toolkit=toolkit,
    llm=llm,
    verbose=True
)

result=sql_agent.invoke(Question)

print(result)

if st.button("Run Query"):
    if Question:  
        query=SQL_PREFIX+Question
        # +SQL_SUFFIX        
        res=sql_agent.invoke(query)
      
        st.write("### Final Answer")
        st.markdown(res["output"])
    else:
        st.error("Please enter your question")    




