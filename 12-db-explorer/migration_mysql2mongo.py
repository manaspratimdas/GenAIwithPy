import subprocess
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain.prompts import MessagesPlaceholder,HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
from generate_ms_controller import create_ms_controller
from generate_ms_repository import create_ms_repository
from generate_ms_service import create_ms_service
from generate_ms_pom import create_ms_pom



def read_file_to_variable(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content

# Example usage:
filename = "Questions_and_Results.txt"
text_content = read_file_to_variable(filename)
print(text_content)

load_dotenv()

llm = OpenAI()  


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

prompt_prefix=f"""
    
    You are a  mongodb database expert.

    You have the following context to create mongodb database : {text_content}

     
 
    
    
    """
prompt_specific_requiremen="""
   
   Take into account you will be using MongoDB 6.0.

    """

prompt_suffix="""

    Ensure that data stored in the MongoDB is in the format of BSON documents. 
    
    remove the special charatecter such as triple backticks from the content

   
    """


question_results = {}


question2="""


    Create MongoDB database collections. Use the proper naming convention for the MongoDB database collections.
    Inside of the collection create  documents as required.
    Inside of the document create  fields as required 
    Mongodb should be allowed to store nested data wherever required
    
   
           
       """

#   Generate 10 sample documents for each collection.

content=f"""     
                {prompt_prefix}                                            
                {question2} 
                {prompt_specific_requiremen}
             
    
            """
# {prompt_suffix}
print(content)

result = chain({"content": content})
question_results[question2] = result["text"]  
print(result["text"]) 

with open("sql2mongodb_migration_script.txt", "w") as file:
        file.write(result["text"])
