from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from dotenv import load_dotenv


load_dotenv

embeddings = OpenAIEmbeddings()


text_splitter=CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=0
)


loader=TextLoader("Questions_and_Results.txt")
docs=loader.load_and_split(
    text_splitter=text_splitter
)


db=Chroma.from_documents(
    docs,
    embedding=embeddings,
    persist_directory="db-explorer"

)

