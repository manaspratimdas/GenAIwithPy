import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from pinecone_setup import vectorstore
from dotenv import load_dotenv


# Load environment variables


load_dotenv()

# embeddings = OpenAIEmbeddings()

llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

output_parser =StrOutputParser()



# Ensure the mock pwd module is used on Windows
if os.name != 'posix':
    import sys
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))  # Adjust path as necessary



# Define a function to get the current username based on the OS
def get_username():
    if os.name == 'posix':
        import pwd
        return pwd.getpwuid(os.getuid())[0]
    else:
        # Use the mock pwd module on Windows
        import pwd
        return pwd.getpwuid(0).pw_name  # Assuming 0 is the uid for the mock


# Initialize text splitter with specified chunk size and overlap
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)

# Load PDF using PyPDFLoader
loader = PyPDFLoader("myresume.pdf")

# Load and split the document using the defined text splitter
docs = loader.load_and_split(text_splitter)

# Print the split documents
print(docs)

# Optionally, print the current user (demonstrates usage of get_username function)
# print(f"Current user is: {get_username()}")

for doc in docs:
    doc.metadata={
        "page": doc.metadata["page"],
        "text": doc.page_content,
        "pdf_id": "resume-1"
    }



vectorstore.add_documents(docs)

# print("done")

# # QA startes from here

# retriever = vectorstore.as_retriever()

# contextualize_q_system_prompt = (
#     "Given a chat history and the latest user question "
#     "which might reference context in the chat history, "
#     "formulate a standalone question which can be understood "
#     "without the chat history. Do NOT answer the question, "
#     "just reformulate it if needed and otherwise return it as is."
# )

# #question_maker_prompt
# contextualize_q_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", contextualize_q_system_prompt),
#         MessagesPlaceholder(variable_name="chat_history"),
#         ("human", "{question}"),
#     ]
# )


# question_chain = contextualize_q_prompt | llm | StrOutputParser()

# # print(question_chain)

# system_prompt = (
#     "You are an assistant for question-answering tasks. "
#     "Use the following pieces of retrieved context to answer "
#     "the question. If you don't know the answer, say that you "
#     "don't know. Use three sentences maximum and keep the "
#     "answer concise."
#     "\n\n"
#     "{context}"
# )

# qa_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_prompt),
#         MessagesPlaceholder("chat_history"),
#         ("human", "{question}"),
#     ]
# )

# def contextualized_question(input: dict):
#     if input.get("chat_history"):
#         return question_chain
#     else:
#         return input["question"]
    

# retriver_chain = RunnablePassthrough.assign(
#     context=contextualized_question | retriever
# )

# # retriver_chain.invoke({
# #     "chat_history": [HumanMessage(content="whose in Manas")],
# #     "question": "how much experience he has?"

# # })

# rag_chain=(
#         retriver_chain 
#         | qa_prompt
#         | llm
#         # | output_parser
        
#         )


# print("*************************************************")

# class HumanMessage:
#     def __init__(self, content):
#         self.content = content


# rag_chain=(
#         retriver_chain 
#         | qa_prompt
#         | llm
#         # | output_parser
        
#         )

# while True:
#     question = input("Enter a question (type 'exit' to quit): ")
#     chat_history=[]
#     if question.lower() == 'exit':
#         break


    
#     ai_msg = rag_chain.invoke({
#         "question": question,
#         "chat_history": chat_history
#     })
    
#     chat_history.extend([HumanMessage(content=question), ai_msg])
    
#     print(ai_msg.content)
#     print("*************************************************")

