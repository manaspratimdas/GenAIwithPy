import subprocess
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain.prompts import MessagesPlaceholder,HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI



def create_ms_controller(bounded_context, prompt_prefix, prompt_suffix,prompt_specific_requiremen):
    print(bounded_context)
    print("++++++++++++++++++++++++++++++++++++++++++++++++++")
    # print(prompt_prefix)
    # print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
    # print(prompt_suffix)

    load_dotenv()

    # llm = OpenAI()  

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

    question_results = {}


    # controller

    question3="""
        Create the content of the controller.java class. Name of the controller class is {}Controller.java
        Controller is a rest controller.
        provide implementation for all the request mapping.
        It should have request handling methods. 
        These methods typically have parameters to receive request data, such as path variables, query parameters, or request bodies and
        return a value that represents the response to be sent back to the client.
        Controllers can handle exceptions using annotations to provide custom error responses.      
        The controller class inject service class and invoke the method from the service class. 
        
        The code should follow the best practice in terms of error and exception handling, logging, comment. 
        Important: Remove triple backticks from the content at the begining and end of generated content.
        create a proper formated jave file. 

        """.format(bounded_context)
    
    content=f"""     
                {prompt_prefix}                                            
                {question3} 
                {prompt_suffix}
            """

    result = chain({"content": content})
    question_results[question3] = result["text"]  
    print(result["text"]) 

    path=f"sakiladb.{bounded_context}/src/main/java/com/{bounded_context}/{bounded_context}Controller.java"
    print(path)

    with open(path, "w") as file:
        file.write(result["text"])

      









