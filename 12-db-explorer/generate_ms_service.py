import subprocess
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain.prompts import MessagesPlaceholder,HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI



def create_ms_service(bounded_context, prompt_prefix, prompt_suffix,prompt_specific_requiremen):
    print(bounded_context)

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

  


    question4="""
        Create the content of the service.java class.  Name of the service class is {}Service.java
        This class will contain Business Logic, Statelessness,Transaction Management,Interaction with Repositories
        The Service class inject repository class and invoke the method from the repository class. 
        The code should follow the best practice in terms of error and exception handling, logging, comment. 
        create a proper formated jave file. 
        Important: Remove triple backticks from the content at the begining and end of generated content.

    """.format(bounded_context)  

    content=f"""     
                {prompt_prefix}                                            
                {question4} 
                {prompt_suffix}
            """

    result = chain({"content": content})
    question_results[question4] = result["text"]  
    print(result["text"]) 

    path=f"sakiladb.{bounded_context}/src/main/java/com/{bounded_context}/{bounded_context}Service.java"
    print(path)

    with open(path, "w") as file:
        file.write(result["text"])  

          









