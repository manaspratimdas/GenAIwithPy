import os
from langchain_pinecone import PineconeVectorStore
from langchain.vectorstores import pinecone
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

chat=ChatOpenAI()
embeddings=OpenAIEmbeddings()


pinecone_api_key = os.getenv('PINECONE_API_KEY')
pinecone_env_name = os.getenv('PINECONE_ENV_NAME')

index_name = "mpddocs"

vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)

# print(vectorstore)