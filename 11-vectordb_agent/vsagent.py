from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

llm = OpenAI(temperature=0)

from pathlib import Path

relevant_parts = []
for p in Path(".").absolute().parts:
    relevant_parts.append(p)
    if relevant_parts[-3:] == ["langchain", "docs", "modules"]:
        break
# doc_path = str(Path(*relevant_parts) / "database_details.txt")
doc_path = "database_details.txt"


from langchain_community.document_loaders import TextLoader

loader = TextLoader(doc_path)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

print(texts)

embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings, collection_name="movies")

movies_rag = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff", retriever=docsearch.as_retriever()
)


from langchain.agents import AgentType, Tool, initialize_agent
from langchain_openai import OpenAI

tools = [
    Tool(
        name="Movies in System",
        func=movies_rag.run,
        description="useful for when you need to answer questions about movies. Input should be a fully formed question.",
    ),
    # Tool(
    #     name="Ruff QA System",
    #     func=ruff.run,
    #     description="useful for when you need to answer questions about ruff (a python linter). Input should be a fully formed question.",
    # ),
]


agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent.run(
    "How is the domian of the syetem "
)

