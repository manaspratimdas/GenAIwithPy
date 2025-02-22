import subprocess
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain.prompts import MessagesPlaceholder,HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI



def create_ms_repository(bounded_context, prompt_prefix, prompt_suffix,prompt_specific_requiremen):
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

    
    question5="""
        Create the content of the Repository.java class.  Name of the repository class is {}Repository.java
        This class will privide Data Access Abstraction, Spring Data Integration, Transaction Management, Domain-Driven Design
        Repository class should contain the database operation method
        The code should follow the best practice in terms of error and exception handling, logging, comment. 
        create a proper formated jave file.
        Important: Remove triple backticks from the content at the begining and end of generated content.


    """.format(bounded_context)  

    content=f"""     
                {prompt_prefix}                                            
                {question5} 
                {prompt_specific_requiremen}
                {prompt_suffix}
            """

    result = chain({"content": content})
    question_results[question5] = result["text"]  
    print(result["text"]) 

    path=f"sakiladb.{bounded_context}/src/main/java/com/{bounded_context}/{bounded_context}Repository.java"
    print(path)

    with open(path, "w") as file:
        file.write(result["text"])          









