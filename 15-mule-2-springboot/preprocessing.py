import json
import xmltodict
from langchain_community.document_loaders import JSONLoader
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain.prompts import MessagesPlaceholder,HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI


with open("http-restful-resource.xml") as xml_file:
	
	data_dict = xmltodict.parse(xml_file.read())
	
	json_data = json.dumps(data_dict)
	
	# # Write the json data to output 
	# # json file
	# with open("http-restful-resource.json", "w") as json_file:
	# 	json_file.write(json_data)
		
load_dotenv()

llm = OpenAI()     

prompt_prefix=f"""
    
    You have the folowing infromation in json format: {json_data}

    You are a migration expert whose job is to migrate from mulesfot.
    
    """
prompt_suffix="""

    While answering the above questions provide as much details

    """

question_results = {}

  
question1="Provide description what is the code in json is doing"
question2="Explain in simple and plain language what the application is doing"
question3="A step-by-step guide on how to accomplish this task"
question4="Identify the domain and the bounded context"



questions_array = [
         question1,
        question2,
        question3,       
        question4
        ]



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


with open("http-restful-resource.txt", "w") as file:
        file.write(" All questions and results:\n")
        for question, result in question_results.items():
            file.write(f"Question: {question}, Result: {result}\n")

print("Text file has been created and saved")

