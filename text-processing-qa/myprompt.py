from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

chat=ChatOpenAI()
embeddings=OpenAIEmbeddings()

db=Chroma(
    persist_directory="emb",
    embedding_function=embeddings
)

retriever=db.as_retriever()

chain=RetrievalQA.from_chain_type(
    llm=chat,
    retriever=retriever,
    chain_type="stuff"
)



result =chain.run("tell some fact about Eiffel Tower")

print(result)
