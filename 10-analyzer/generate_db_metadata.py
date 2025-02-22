import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine,MetaData, inspect

# from langchain.tools import DatabaseTool, DataExplorerTool, DataQualityTool 
# from langchain.agents import AgentExecutor
# import pymysql  # If using PyMySQL
# # # clearclarcfrom langchain.chains import SQLDatabaseSequentialChain
# from langchain_community.utilities import SQLDatabase
# from langchain_experimental.sql import SQLDatabaseChain



# import pandas as pd

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
engine = create_engine(pg_uri) 

db = SQLDatabase(engine)

metadata = MetaData()

metadata.reflect(bind=engine)

inspector = inspect(engine)



    # Get list of tables:

# tables = inspector.get_table_names()
# # print(tables)
# # Specify the name of the file to be created

# for table in tables:
#         columns = inspector.get_columns(table) 
#         print(table)
#         print(columns)
#         index=inspector.get_indexes(table)
#         print(index)
#         print(inspector.get_foreign_keys(table))



       
#         print(inspector.get_multi_foreign_keys() )

#         print(inspector.get_materialized_view_names)

#         print(inspector.get_multi_indexes())

#         print(inspector.get_multi_columns())

# Open a file in write mode. If the file doesn't exist, it will be created.
with open('database_details.txt', 'w') as file:
    tables = inspector.get_table_names()
 
    for table in tables:
           print(table)
           file.write(f"Table: {table}")
        

        #   Retrieve column details for the current table
           columns = inspector.get_columns(table)
    #     # Write the table name followed by its columns to the file
           file.write(f"Table: {table}\nColumns: {columns}\n")
        
    #     # Retrieve index details for the current table
           index = inspector.get_indexes(table)
    #     # Write index details to the file
           file.write(f"Indexes: {index}\n")
        
    #     # Retrieve foreign key details for the current table
           foreign_keys = inspector.get_foreign_keys(table)
    #     # Write foreign key details to the file
           file.write(f"Foreign Keys: {foreign_keys}\n")
        
    #     # Additional database details
    multi_foreign_keys = inspector.get_multi_foreign_keys()
    file.write(f" multi_foreign_keys: { multi_foreign_keys}\n")
    # # materialized_view_names = inspector.get_materialized_view_names()
    multi_indexes = inspector.get_multi_indexes()
    file.write(f" multi_indexes: { multi_indexes}\n")
    multi_columns = inspector.get_multi_columns()
    file.write(f" multi_columns: { multi_columns}\n")

 


   

















# db = SQLDatabase.from_uri(pg_uri)


# toolkit=SQLDatabaseToolkit(
#     db=db,
#     llm=llm
#     )

# print(db.get_usable_table_names())

# tables=db.get_usable_table_names()

# for table in tables:
#     print(table)



# print(db.get_table_info())

# db_info=db.get_table_info()

# print(db_info)

# data_explorer_tool = DataExplorerTool(
# "explore_data", 
# "Describe the data in table '{table_name}'"
# )


# memory = ConversationMemory(llm=llm)
# agent = AgentExecutor.from_llm_and_tools(
# llm=llm, 
# tools=[data_explorer_tool],
# memory=memory,
# agent_type="zero-shot-react-description"
# )







# # result =toolkit.get_tools()

# # print(result)

# # PROMPT = """ 
# # Given an input question, first create a syntactically correct mysql query to run,  
# # then look at the results of the query and return the answer.  
# # The question: {question}
# # """

# # # db_chain = SQLDatabaseSequentialChain(llm=llm, database=db, verbose=True, top_k=3)
# # # db_chain = SQLDatabaseChain.from_llm(llm, db)
# # # question = "List the top 5 actors" 
# # # # use db_chain.run(question) instead if you don't have a prompt
# # # result=db_chain.invoke(
# # #     PROMPT.format(question=question)
# # #     ) 

# # # print(result)

# # SQL_PREFIX = """You are a MySQL expert. Given an input question, first create a syntactically correct SQLite query to run, then look at the results of the query and return the answer to the input question.
# # Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.
# # Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
# # Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
# # Pay attention to use date('now') function to get the current date, if the question involves "today".
# # """

# # # SQL_SUFFIX=""" 
# # # Preset the answer in human natural language. 
# # # """

# # Question=st.text_input("Ask your question here: ")



# # toolkit=SQLDatabaseToolkit(
# #     db=db,
# #     llm=llm
# #     )

# # sql_agent=create_sql_agent(
# #     toolkit=toolkit,
# #     llm=llm,
# #     verbose=True
# # )

# # result=sql_agent.invoke(Question)

# # print(result)

# # if st.button("Run Query"):
# #     if Question:  
# #         query=SQL_PREFIX+Question
# #         # +SQL_SUFFIX        
# #         res=sql_agent.invoke(query)
      
# #         st.write("### Final Answer")
# #         st.markdown(res["output"])
# #     else:
# #         st.error("Please enter your question")    




