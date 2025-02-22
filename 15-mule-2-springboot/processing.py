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
    
    You have the folowing context which will be used to create a cloud native solution: {text_content}

    You are AWS cloud developer who is expert is creating a cloud native solution using the language of java. 
    
    The solution that you will build will be deployed in AWS cloud. 

    The java project that you will be creating is a maven project.
    
    The business logic will be a aws lambda function. 
    
       
    """
prompt_suffix="""

    Please provide the necessary Maven dependencies, taking into account that I am using:
    org.springframework.boot spring-boot-starter-parent 2.1.5.RELEASE and Java 11

    """

question_results = {}


question1="Generate the Maven command to create a new Spring Boot application."
question2="Create the pom.xml file."
question3="Create the content of the handler.java class"
question4="Create the content of the Service.java class"
question5="Create the content of the Configuration.java class"
question6="Create the content of the repository.java class"
# question7="Create the content of the utility.java class"
# question8="""
# Create the unit test cases
# """






questions_array = [
         question1,
        question2,
        question3,       
        question4,
        question5,
        question6
        # question7    
        #  question8
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


with open("http-restful-resource.txt", "a") as file:
        file.write(" All questions and results:\n")
        for question, result in question_results.items():
            file.write(f"Question: {question}, Result: {result}\n")

print("Text file has been created and saved")



