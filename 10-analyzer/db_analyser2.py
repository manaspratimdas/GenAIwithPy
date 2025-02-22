import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_community.agent_toolkits.sql.toolkit import  SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import pymysql  # If using PyMySQL
# clearclarcfrom langchain.chains import SQLDatabaseSequentialChain
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain


load_dotenv()

llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# output_parser =StrOutputParser()

# st.title("SQL DB Agent Implementation using Langchain")

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

# Question=st.text_input("Ask your question here: ")
Question1="What are the primary keys in each table, and how do they relate to one another?"
Question2="Are there any foreign key constraints in place, indicating relationships between different tables?"
Question3="How are entities represented in the database, and what attributes do they possess?"
Question4="Are there any normalization techniques applied to the database design, and if so, how do they impact the relationships between tables?"
Question5="Do any tables exhibit inheritance or specialization relationships, and if yes, how are they implemented?"
Question6="Are there any junction tables present to facilitate many-to-many relationships between entities?"
Question7="How do the tables in the database reflect the overall business logic and requirements of the system they represent?"
Question8="What are the primary keys in each table, and how do they relate to one another?"
Question9="I want to use the database for domain driven design. How can I do?"
Question10="Infer the bounded context from the data model and elaborate"
Question11="the ubiquitous language of thr bounded context from the data model and elaborate"
Question12="Can you explain the key business processes and goals that the database is intended to support?"
Question13="What are the main entities or objects in the domain, and how do they relate to each other?"



toolkit=SQLDatabaseToolkit(
    db=db,
    llm=llm
    )


sql_agent=create_sql_agent(
    toolkit=toolkit,
    llm=llm,
    verbose=True
)

try:
    result_q1 = sql_agent.invoke(Question1)
except Exception as e:
    print(f" {Question1}:  An error occurred while invoking SQL Agent")
    result_q1 = None  # Optionally set a default value or handle the error as needed

try:
    result_q2 = sql_agent.invoke(Question2)
except Exception as e:
    print(f" {Question2}:  An error occurred while invoking SQL Agent")
    result_q2 = None  # Optionally set a default value or handle the error as needed

try:
    result_q3 = sql_agent.invoke(Question3)
except Exception as e:
    print(f" {Question3}:  An error occurred while invoking SQL Agent")
    result_q3 = None  # Optionally set a default value or handle the error as needed

try:
    result_q4 = sql_agent.invoke(Question4)
except Exception as e:
    print(f" {Question4}:  An error occurred while invoking SQL Agent")
    result_q4 = None  # Optionally set a default value or handle the error as needed

try:
    result_q5 = sql_agent.invoke(Question5)
except Exception as e:
    print(f" {Question5}:  An error occurred while invoking SQL Agent")
    result_q5 = None  # Optionally set a default value or handle the error as needed

try:
    result_q6 = sql_agent.invoke(Question6)
except Exception as e:
    print(f" {Question6}:  An error occurred while invoking SQL Agent")
    result_q6 = None  # Optionally set a default value or handle the error as needed

try:
    result_q7 = sql_agent.invoke(Question7)
except Exception as e:
    print(f" {Question7}:  An error occurred while invoking SQL Agent")
    result_q7 = None  # Optionally set a default value or handle the error as needed

try:
    result_q8 = sql_agent.invoke(Question8)
except Exception as e:
    print(f" {Question8}:  An error occurred while invoking SQL Agent")
    result_q8 = None  # Optionally set a default value or handle the error as needed    

try:
    result_q9 = sql_agent.invoke(Question9)
except Exception as e:
    print(f" {Question9}:  An error occurred while invoking SQL Agent")
    result_q9 = None  # Optionally set a default value or handle the error as needed    


try:
    result_q10 = sql_agent.invoke(Question10)
except Exception as e:
    print(f" {Question10}:  An error occurred while invoking SQL Agent")
    result_q10 = None  # Optionally set a default value or handle the error as needed        

try:
    result_q11 = sql_agent.invoke(Question11)
except Exception as e:
    print(f" {Question11}:  An error occurred while invoking SQL Agent")
    result_q11 = None  # Optionally set a default value or handle the error as needed   

try:
    result_q12 = sql_agent.invoke(Question12)
except Exception as e:
    print(f" {Question12}:  An error occurred while invoking SQL Agent")
    result_q12 = None  # Optionally set a default value or handle the error as needed    

try:
    result_q13 = sql_agent.invoke(Question13)
except Exception as e:
    print(f" {Question13}:  An error occurred while invoking SQL Agent")
    result_q13 = None  # Optionally set a default value or handle the error as needed    





        








        

# result_q2=sql_agent.invoke(Question2)
# result_q3=sql_agent.invoke(Question3)
# #result_q4=sql_agent.invoke(Question4)
# # result_q5=sql_agent.invoke(Question5)
# result_q6=sql_agent.invoke(Question6)
# result_q7=sql_agent.invoke(Question7)
# result_q8=sql_agent.invoke(Question8)
# result_q9=sql_agent.invoke(Question9)
# # result_q10=sql_agent.invoke(Question10)
# result_q12=sql_agent.invoke(Question12)
# result_q13=sql_agent.invoke(Question13)




# print(result)

with open('database_details_11.txt', 'a') as file:
        file.write(f"{result_q1}\n")
        file.write(f"{result_q2}\n")
        file.write(f"{result_q3}\n")
        file.write(f"{result_q4}\n")
        file.write(f"{result_q5}\n")
        file.write(f"{result_q6}\n")
        file.write(f"{result_q7}\n")
        file.write(f"{result_q8}\n")
        file.write(f"{result_q9}\n")
        file.write(f"{result_q12}\n")
        file.write(f"{result_q13}\n")
        file.write(f"{result_q10}\n")



# sql_agent_2=create_sql_agent(
#     toolkit=toolkit,
#     llm=llm,
#     verbose=True
# )

# result_q12=sql_agent.invoke(Question12)

# with open('database_details.txt', 'a') as file:
#         # file.write(f"{result_q9}\n")
#         file.write(f"{result_q12}\n")

    # tables = inspector.get_table_names()
 
    # for table in tables:
    #        print(table)
    #        file.write(f"Table: {table}")
        

    #     #   Retrieve column details for the current table
    #        columns = inspector.get_columns(table)
    # #     # Write the table name followed by its columns to the file
    #        file.write(f"Table: {table}\nColumns: {columns}\n")
        
    # #     # Retrieve index details for the current table
    #        index = inspector.get_indexes(table)
    # #     # Write index details to the file
    #        file.write(f"Indexes: {index}\n")
        
    # #     # Retrieve foreign key details for the current table
    #        foreign_keys = inspector.get_foreign_keys(table)
    # #     # Write foreign key details to the file
    #        file.write(f"Foreign Keys: {foreign_keys}\n")
        
    # #     # Additional database details
    # multi_foreign_keys = inspector.get_multi_foreign_keys()
