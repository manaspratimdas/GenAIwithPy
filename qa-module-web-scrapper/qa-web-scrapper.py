import os
import datetime
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.document_loaders import FireCrawlLoader
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# embeddings = OpenAIEmbeddings()

llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

output_parser =StrOutputParser()

firecrawler_api_key = os.getenv('FIRECRAWL_API_KEY')

loader = FireCrawlLoader(url="https://firecrawl.dev", mode="crawl")

# docs = loader.load()

# docs[0]

# print(docs)

pages = []
for doc in loader.lazy_load():
    pages.append(doc)
    if len(pages) >= 10:
        # do some paged operation, e.g.
        # index.upsert(page)

        pages = []

# len(pages)        

# docs = []
# docs_lazy = loader.lazy_load()

# # async variant:
# # docs_lazy = await loader.alazy_load()

# for doc in docs_lazy:
#     docs.append(doc)
# print(docs[0].page_content[:100])
# print(docs[0].metadata)

# print(docs)


