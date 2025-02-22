import subprocess
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain.prompts import MessagesPlaceholder,HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI


def read_file_to_variable(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content

# Example usage:
filename = "http-restful-resource.txt"
text_content = read_file_to_variable(filename)
print(text_content)

load_dotenv()

llm = OpenAI()  

prompt_prefix=f"""
    
    You are an expert java developer who is experienced in creating spring boot maven project. 

    You have the following context which will be used create spring boot maven project: {text_content}
  
    Review the content in the context to create important classes in a spring boot maven project.
 
    The code should follow the best practice in terms of error and exception handling, logging, comment. 


    Take into  account that you are using: org.springframework.boot spring-boot-starter-parent 2.1.5.RELEASE and Java 11
    
    """
prompt_suffix="""

    Recheck the code  and maven dependencies to ensure that there is no syntax error.  
    Remove triple backticks from the content.  

    """


question_results = {}

groupId="com.demo"
artifactId="mule-spring-app"
question1="""
            Generate the Maven command to create a new Spring Boot application.
          
            The command will be used Programmatically so while executing the command there will be no human intervention 

        """

question2="""
          Create the pom.xml file. Inspect the content code generated for all the class to determine dependencies
          Maven dependencies for all the classes should be included.

          create a proper formated xml file. 
          example of proper formate xml is
          <project xmlns...>
          </project>

          Remove triple backticks from the content
"""




question3="""
        Create the content of the handler.java class.
        The handler class must implement one of the predefined functional interfaces provided by the AWS Lambda Java runtime
        It receives the input event, processes it, and returns the output. It should invoke 
        The handler class inject service class and invoke the method from the service class. 
        create a proper formated jave file. 
        The code should follow the best practice in terms of error and exception handling, logging, comment. 
         Remove triple backticks from the content



"""

question4="""
        Create the content of the service.java class.  
        This class will contain Business Logic, Statelessness,Transaction Management,Interaction with Repositories
        The Service class inject repository class and invoke the method from the repository class. 
        The code should follow the best practice in terms of error and exception handling, logging, comment. 
        create a proper formated jave file.Remove triple backticks from the content

"""

question5="""
        Create the content of the Repository.java class.  
        This class will privide Data Access Abstraction, Spring Data Integration, Transaction Management, Domain-Driven Design
        Repository class should contain the database operation method
        The code should follow the best practice in terms of error and exception handling, logging, comment. 
        create a proper formated jave file.Remove triple backticks from the content

"""






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






content=f"""                                                 
                {question1} 
            """

result = chain({"content": content})
question_results[question1] = result["text"]  
print(result["text"]) 

subprocess.call(result["text"], shell=True)

# handlerclass

content=f"""     
                {prompt_prefix}                                            
                {question3} 
                {prompt_suffix}
            """

result = chain({"content": content})
question_results[question3] = result["text"]  
print(result["text"]) 

with open("my-spring-boot-app/src/main/java/com/example/myHandler.java", "w") as file:
        file.write(result["text"])


# service class
content=f"""     
                {prompt_prefix}                                            
                {question4} 
                {prompt_suffix}
            """

result = chain({"content": content})
question_results[question4] = result["text"]  
print(result["text"]) 

with open("my-spring-boot-app/src/main/java/com/example/myService.java", "w") as file:
        file.write(result["text"])    


# repository class

content=f"""     
                {prompt_prefix}                                            
                {question5} 
                {prompt_suffix}
            """

result = chain({"content": content})
question_results[question5] = result["text"]  
print(result["text"]) 

with open("my-spring-boot-app/src/main/java/com/example/myRepository.java", "w") as file:
        file.write(result["text"])    




# pom.xml


content=f"""     
                {prompt_prefix}                                            
                {question2} 
                {prompt_suffix}
            """

result = chain({"content": content})
question_results[question2] = result["text"]  
print(result["text"]) 

with open("my-spring-boot-app/pom.xml", "w") as file:
        file.write(result["text"])







