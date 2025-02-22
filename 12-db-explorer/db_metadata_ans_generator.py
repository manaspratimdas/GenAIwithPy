import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from question_generator import generate_database_questions

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

username = os.getenv('username')
password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')
mydatabase = os.getenv('mydatabase')

pg_uri = f"mysql+pymysql://root:{password}@localhost:3306/sakila"
db = SQLDatabase.from_uri(pg_uri)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
sql_agent = create_sql_agent(toolkit=toolkit, llm=llm, verbose=True)

def generate_formatted_results():
    load_dotenv()



    questions = generate_database_questions()
    formatted_results = []

    for question in questions:
        try:
            answer = sql_agent.invoke(question)
        except Exception as e:
            print(f"{question}: An error occurred while invoking SQL Agent")
            answer = "An error occurred, unable to retrieve answer."

        formatted_results.append({"question": question, "answer": answer})

    return formatted_results
