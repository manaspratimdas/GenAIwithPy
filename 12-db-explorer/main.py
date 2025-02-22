# main.py
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from question_generator import generate_database_questions
from langchain.prompts import MessagesPlaceholder,HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
from fpdf import FPDF
from db_metadata_generator import list_database_tables
from db_metadata import get_db_table_info
from db_metadata_ans_generator import generate_formatted_results

load_dotenv()

llm = OpenAI()

def main():
    # questions = generate_database_questions()
    # for question in questions:
    #     print(question)

    tables = list_database_tables()
    # for table in tables:
    #     print(table) 


     # Generate formatted results from SQL queries
    results = generate_formatted_results()
    formatted_output = "Results from SQL Queries:\n"
    for result in results:
        formatted_output += f"Question: {result['question']}\nAnswer: {result['answer']}\n\n"

    # Get database table information and format it
    graph_details = get_db_table_info()
    # formatted_output += "Graph Details:\n"
    # formatted_output = graph_details

    # Print the complete formatted output
    # print(formatted_output)
  
 
    
    prompt_prefix=f"""

    You have the following information:
	List of tables : {tables},
	The relationship between tables in form of nodes and edges: {graph_details},
	and some question and answer about the database: {formatted_output}

    You are a data architect use the above information to answer the following question.
    
    """

    prompt_suffix="""

    While answering the above questions provide as much details

    """

 
    question_results = {}

  
    question1="The domain and various bounded contexts ."
    question2="Interrelationships between the bounded contexts."
    question3="Details of ubiquitous language that can be used for  shared vocabulary that is used by all stakeholders "
    question4="Provide a detailed breakdown of how each table is related to each other based on the provided information"
    question5="derive a list of REST API endpoints that can be created to interact with the system"
    question6="Create Swagger document outlining the REST API endpoints based on the information provided"

#     # Create an array (list in Python) with the questions
    questions_array = [
         question1,
        question2, question3,
                       question4, question5, question6]

#     # Print the array to verify its contents
    print(questions_array)

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


    # Initialize a dictionary to store questions and their results
 

# Iterate over the array of questions using a for loop
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


    with open("Questions_and_Results.txt", "w") as file:
        file.write(" All questions and results:\n")
        file.write(f"List of tables in database :\n {tables}\n")
        file.write(f"The relationship between tables in form of nodes and edges: \n{graph_details}\n")
        file.write(f"Imprtant information about the database : \n{formatted_output}\n")
        for question, result in question_results.items():
            file.write(f"Question: {question}, Result: {result}\n")

    print("Text file has been created and saved as 'Questions_and_Results.txt'")



# # Create instance of FPDF class
#     pdf = FPDF()

# # Add a page
#     pdf.add_page()

# # Set font
#     pdf.set_font("Arial", size = 12)

# # Iterate over the dictionary and add to PDF
#     for question, result in question_results.items():
#         pdf.cell(200, 10, txt = f"Question: {question}", ln = True)
#         pdf.cell(200, 10, txt = f"Result: {result}", ln = True)
#         pdf.cell(200, 10, txt = "", ln = True)  # Add a blank line for spacing

# # Save the pdf with name .pdf
#     pdf.output("Questions_and_Results.pdf")

#     print("PDF file has been created and saved as 'Questions_and_Results.pdf'")
   











    

    # chain = prompt_template.pipe(llm)
    # db_info_1 = chain.invoke(input=formatted_output)
    # print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    # print(db_info_1)

    

    # formatted_output = f"""
    #     Tables in database are: {tables}.
    #     Nodes representing database tables and relationships: {formatted_output}.
    #     Additional information: {db_info_level_1}

    #     """
    
    # print(formatted_output)

    # prompt_template = PromptTemplate.from_template("""
    # As a data architect,
    # you are provided with input data consisting of tables in database,  nodes representing database tables 
    # and relationships indicating connections between these tables, along with details about the relationships 
    # and interconnected attributes. Your goal is to analyze this data to create detailed content illustrating
    # the relationships between database tables and how they are related. This analysis will help identify:

    # The domain and various bounded contexts.
    # Interrelationships between the bounded contexts.
    # The REST API that can be generated using this information.
    # The data model migration to modern databases like NoSQL or graph SQL.

                                                   
    # The input is {formatted_output}                                               

    # """)

    # chain = prompt_template.pipe(llm)
    # db_info_level_2 = chain.invoke(input=formatted_output)
    # print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    # print(db_info_level_2)




    # Identify the domain and various bounded contexts within the data.
    # Explore the interrelationships between different bounded contexts. 
    # Subdomain within the domain business context also the ubiquitous language used around these bounded context
    






        
          

if __name__ == '__main__':
    main()
