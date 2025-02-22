from langchain_community.document_loaders import JSONLoader
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain.prompts import MessagesPlaceholder,HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI

import json
from pathlib import Path
from pprint import pprint

load_dotenv()

llm = OpenAI()


file_path='importing-a-csv-file-into-ms-sharepoint.json'
data = json.loads(Path(file_path).read_text())

pprint(data)


prompt_prefix=f"""
    
    You have the folowing infromation in json format: {data}

    You are a migration expert whose job is to migrate from mulesfot.
    
    """
prompt_suffix="""

    While answering the above questions provide as much details

    """


question_results = {}

  
question1="provide description what is the code in json is doing"
question2="generate the pseudocode."
question3="convert the following into java code snippet"
# question4="""

# convert the above code into a springboot application. 
# create the pom.xml file with the required dependency. 
# Also create the proper controller class, servie class and configuration class"

# """
question5="""
 Convert the application into AWS lambda function. 
 The application will be deployed in the aws platform. 
 Ensure that application follow the best practice and a modular approach,
 Generate test cases as well. 
 The programming language is java. 

"""

questions_array = [
         question1,
        question2,
        question3,
        # question4,
        question5]



chat=ChatOpenAI()

memory=ConversationBufferMemory(memory_key="messages", return_messages=True)


prompt=ChatPromptTemplate(
    input_variables =["content","messages"],
     messages=[
         MessagesPlaceholder(variable_name="messages"),
         HumanMessagePromptTemplate.from_template("{content}")
     ]

    )

chain=LLMChain(
         llm=chat,
         prompt=prompt,
         memory=memory
    )


for question in questions_array:
        print(f">> {question}")  # Simulate user input by printing the question
        content=f"""
                {prompt_prefix}
                                                   
                {question} 
                
                {prompt_suffix}

            """

        try:
        # Process the question. Replace 'chain' with your actual function call if applicable.
            result = chain({"content": content})
            question_results[question] = result["text"]  # Store the result in the dictionary
            # print(result["text"])  # Assuming 'result' is a dictionary with a 'text' key
        except Exception as e:
            print(f"An error occurred: {e}")
            question_results[question] = "none"  # Set the result to "none" in case of an error


with open("importing-a-csv-file-into-ms-sharepoint.txt", "w") as file:
        file.write(" All questions and results:\n")
        for question, result in question_results.items():
            file.write(f"Question: {question}, Result: {result}\n")

print("Text file has been created and saved as 'Questions_and_Results.txt'")

