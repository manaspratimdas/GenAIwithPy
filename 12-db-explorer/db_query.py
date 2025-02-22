import os
from langchain.prompts import PromptTemplate
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
import logging

load_dotenv()

# Assuming `llm` is the instance of ChatOpenAI
def log_llm_call(prompt):
    logging.debug(f"LLM Input: {prompt}")
    response = llm(prompt)
    logging.debug(f"LLM Output: {response}")
    return response
#end of loggin

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

username = os.getenv('username')
password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')
mydatabase = os.getenv('mydatabase')

pg_uri = f"mysql+pymysql://root:{password}@localhost:3306/sakila"

db = SQLDatabase.from_uri(pg_uri)

execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question. You are querying a cad model translated into SQL
    don't include the  sql  in your sql query output
    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    Answer: """
)

chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer_prompt
    | llm
    | log_llm_call  # Use the logging wrapper
    | StrOutputParser()
)

result = chain.invoke({"question": "what is database about"})
print(result)




