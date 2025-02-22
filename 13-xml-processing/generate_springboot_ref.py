import re
from langchain_community.document_loaders import RecursiveUrlLoader
from bs4 import BeautifulSoup

def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()





loader = RecursiveUrlLoader(
    "https://docs.spring.io/spring-boot/reference/",
    prevent_outside=True,
    extractor=bs4_extractor,
    base_url="https://docs.spring.io/spring-boot/reference/",
    link_regex=r'<a\s+(?:[^>]*?\s+)?href="([^"]*(?=index)[^"]*)"',
    # exclude_dirs=['https://docs.python.org/3.9/faq']
)

loader.requests_kwargs = {'verify':False}

docs = loader.load()

# print(docs[0].metadata)

# print(">>>>>>>>>>>>>>>>>>")

# print(docs[1].metadata)

for doc in docs:
     print(">>>>>>>>>>>>>>")
     print(doc.metadata)
     print(">>>>>>>>>>>>>>>>")