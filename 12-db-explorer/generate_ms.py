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
    
    You are an expert java developer who is experienced in creating spring boot maven project. 

    You have the following context which will be used create spring boot maven project: {text_content}
  
    Review the content in the context to create important classes in a spring boot maven project.
 
    The code should follow the best practice in terms of error and exception handling, logging, comment. 

    Take into  account that you are using: org.springframework.boot spring-boot-starter-parent 2.1.5.RELEASE and Java 11.

    
    
    """
prompt_specific_requiremen="""
   
   Take into account you will be using Spring JPA.

    """

prompt_suffix="""

    Recheck the code  and maven dependencies to ensure that there is no syntax error.  
    Remove triple backticks from the content.  

    """


question_results = {}



question2="""
           List all the bounded context in a comma seperated list.Use single word for each bounded context.
           
       """



content=f"""     
                {prompt_prefix}                                            
                {question2} 
                {prompt_suffix}
            """

result = chain({"content": content})
question_results[question2] = result["text"]  
# print(result["text"]) 

# Split the comma-separated list into an array
bounded_contexts = [item.strip() for item in result["text"].split(',')]

# Print the resulting array
# print(bounded_contexts)


for bounded_context in bounded_contexts:

    
    
    question1 = """
            Generate the Maven command to create a new Spring Boot application.
            use groupId=com.{} and artifactId=sakiladb.{}
            use maven-archetype-quickstart:1.0
          
            The command will be used Programmatically so while executing the command there will be no human intervention 
        """.format(bounded_context, bounded_context)

    print(question1)

    content=f"""                                                 
                {question1} 
            """

    result = chain({"content": content})
    question_results[question1] = result["text"]  
    print(result["text"]) 

    subprocess.call(result["text"], shell=True)


for bounded_context in bounded_contexts:    

    create_ms_controller(bounded_context,prompt_prefix,prompt_suffix,prompt_specific_requiremen)

for bounded_context in bounded_contexts:    

    create_ms_service(bounded_context,prompt_prefix,prompt_suffix,prompt_specific_requiremen)    

for bounded_context in bounded_contexts:    

    create_ms_repository(bounded_context,prompt_prefix,prompt_suffix,prompt_specific_requiremen)  

for bounded_context in bounded_contexts:    

    create_ms_pom(bounded_context,prompt_prefix,prompt_suffix,prompt_specific_requiremen)        


    






# question2="""
#           Create the pom.xml file. Inspect the content code generated for all the class to determine dependencies
#           Maven dependencies for all the classes should be included.

#           create a proper formated xml file. 
#           example of proper formate xml is
#           <project xmlns...>
#           </project>

#           Remove triple backticks from the content
# """




# question3="""
#         Create the content of the controller.java class.
#         Controller is a rest controller.
#         provide implementation for all the request mapping.
#         It should have request handling methods. 
#         These methods typically have parameters to receive request data, such as path variables, query parameters, or request bodies and
#         return a value that represents the response to be sent back to the client.
#         Controllers can handle exceptions using annotations to provide custom error responses.      
#         The controller class inject service class and invoke the method from the service class. 
#         create a proper formated jave file. 
#         The code should follow the best practice in terms of error and exception handling, logging, comment. 
#         Remove triple backticks from the content



# """

# question4="""
#         Create the content of the service.java class.  
#         This class will contain Business Logic, Statelessness,Transaction Management,Interaction with Repositories
#         The Service class inject repository class and invoke the method from the repository class. 
#         The code should follow the best practice in terms of error and exception handling, logging, comment. 
#         create a proper formated jave file.Remove triple backticks from the content

# """

# question5="""
#         Create the content of the Repository.java class.  
#         This class will privide Data Access Abstraction, Spring Data Integration, Transaction Management, Domain-Driven Design
#         Repository class should contain the database operation method
#         The code should follow the best practice in terms of error and exception handling, logging, comment. 
#         create a proper formated jave file.Remove triple backticks from the content

# """














# # handlerclass

# content=f"""     
#                 {prompt_prefix}                                            
#                 {question3} 
#                 {prompt_suffix}
#             """

# result = chain({"content": content})
# question_results[question3] = result["text"]  
# print(result["text"]) 

# with open("sakila-ms/src/main/java/com/example/myHandler.java", "w") as file:
#         file.write(result["text"])


# # service class
# content=f"""     
#                 {prompt_prefix}                                            
#                 {question4} 
#                 {prompt_suffix}
#             """

# result = chain({"content": content})
# question_results[question4] = result["text"]  
# print(result["text"]) 

# with open("sakila-ms/src/main/java/com/example/myService.java", "w") as file:
#         file.write(result["text"])    


# # repository class

# content=f"""     
#                 {prompt_prefix}                                            
#                 {question5} 
#                 {prompt_suffix}
#             """

# result = chain({"content": content})
# question_results[question5] = result["text"]  
# print(result["text"]) 

# with open("sakila-ms/src/main/java/com/example/myRepository.java", "w") as file:
#         file.write(result["text"])    




# # pom.xml


# content=f"""     
#                 {prompt_prefix}                                            
#                 {question2} 
#                 {prompt_suffix}
#             """

# result = chain({"content": content})
# question_results[question2] = result["text"]  
# print(result["text"]) 

# with open("sakila-ms/pom.xml", "w") as file:
#         file.write(result["text"])







