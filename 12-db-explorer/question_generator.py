# question_generator.py
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

def generate_database_questions():
    load_dotenv()

    llm = OpenAI()

    prompt_template = PromptTemplate.from_template("""
    You are a MySQL expert.
    You want to explore the database. Phrase some questions about the database that provide you insight about the database.
    The information that you are seeking not only answers questions but also the domain and bounded context of the database. 
    How the tables are related at a high level. Each question separated by newline.
    """)

    chain = prompt_template.pipe(llm)
    db_questions = chain.invoke({})
    questions_array = db_questions.split('\n')

    return questions_array
