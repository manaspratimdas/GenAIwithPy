# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

chat=ChatOpenAI()
embeddings=OpenAIEmbeddings()

db=Chroma(
    persist_directory="db_info_emb_1",
    embedding_function=embeddings
)

retriever=db.as_retriever()

chain=RetrievalQA.from_chain_type(
    llm=chat,
    retriever=retriever,
    chain_type="stuff"
)



result =chain.run("Can you explain the key business processes and goals that the database is intended to support? ")

print(result)

result =chain.run("what is the key business process ")

print(result)

