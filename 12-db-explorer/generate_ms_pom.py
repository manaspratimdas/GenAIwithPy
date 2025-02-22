import subprocess
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain.prompts import MessagesPlaceholder,HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI



def create_ms_pom(bounded_context, prompt_prefix, prompt_suffix,prompt_specific_requiremen):
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

  


    
    question2="""
          Create the pom.xml file for the {}. Inspect the content code generated for all the class to determine dependencies
          Maven dependencies for all the classes should be included.

          create a proper formated xml file. 
          example of proper formate xml is
          <project xmlns...>
          </project>

          Remove triple backticks from the content
          """.format(bounded_context)  

    content=f"""     
                {prompt_prefix}                                            
                {question2} 
                {prompt_specific_requiremen}
                {prompt_suffix}
            """

    result = chain({"content": content})
    question_results[question2] = result["text"]  
    print(result["text"]) 

    path=f"sakiladb.{bounded_context}/pom.xml"
    print(path)

    with open(path, "w") as file:
        file.write(result["text"])  

          









