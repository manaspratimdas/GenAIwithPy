import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import  SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine


import pandas as pd


load_dotenv()

llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

output_parser =StrOutputParser()

st.title("###SQL DB Agent in LangChian")


database_file_path="customer.db"


engine = create_engine("sqlite:///customers.db")
file_url="customers.csv"
df =pd.read_csv(file_url).fillna(value=0)
df.to_sql("customers", con=engine, if_exists="replace", index=False)

print(f"Database created sucessfully {df.head}",)
st.write({df.head})



SQL_PREFIX = """You are a SQLite expert. Given an input question, first create a syntactically correct SQLite query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use date('now') function to get the current date, if the question involves "today".


"""


SQL_SUFFIX="""

Present the answer in a tabular format. Also put the heading for each column.

"""


question=st.text_input("Ask your question here: ")

db=SQLDatabase.from_uri("sqlite:///customers.db")
toolkit=SQLDatabaseToolkit(db=db, llm=llm)

sql_agent=create_sql_agent(
    toolkit=toolkit,
    llm=llm,
    verbose=True
)




if st.button("Run Query"):
    if question:  
        query=SQL_PREFIX+ question + SQL_SUFFIX         
        res=sql_agent.invoke(query)
        st.write("### Final Answer")
        st.markdown(res["output"])
   
    