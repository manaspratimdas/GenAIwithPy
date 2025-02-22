import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage, SystemMessage
from pinecone_setup import vectorstore
from pinecone_emebeding import docs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# embeddings = OpenAIEmbeddings()

llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

output_parser =StrOutputParser()



# vectorstore.add_documents(docs)

# print("done")

retriever = vectorstore.as_retriever()

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

#question_maker_prompt
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)


question_chain = contextualize_q_prompt | llm | StrOutputParser()

# print(question_chain)

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}"),
    ]
)

def contextualized_question(input: dict):
    if input.get("chat_history"):
        return question_chain
    else:
        return input["question"]
    

retriver_chain = RunnablePassthrough.assign(
    context=contextualized_question | retriever
)

retriver_chain.invoke({
    "chat_history": [HumanMessage(content="whose in Manas")],
    "question": "how much experience he has?"

})

rag_chain=(
        retriver_chain 
        | qa_prompt
        | llm
        # | output_parser
        
        )


print("*************************************************")

class HumanMessage:
    def __init__(self, content):
        self.content = content


rag_chain=(
        retriver_chain 
        | qa_prompt
        | llm
        # | output_parser
        
        )

while True:
    question = input("Enter a question (type 'exit' to quit): ")
    chat_history=[]
    if question.lower() == 'exit':
        break


    
    ai_msg = rag_chain.invoke({
        "question": question,
        "chat_history": chat_history
    })
    
    chat_history.extend([HumanMessage(content=question), ai_msg])
    
    print(ai_msg.content)
    print("*************************************************")






