import re
from langchain_community.document_loaders import RecursiveUrlLoader
from bs4 import BeautifulSoup

def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()



# loader = RecursiveUrlLoader(
#     "https://docs.python.org/3.9/",
#     extractor=bs4_extractor,
#     # max_depth=2,
#     # use_async=False,
#     # extractor=None,
#     # metadata_extractor=None,
#     # exclude_dirs=(),
#     # timeout=10,
#     # check_response_status=True,
#     # continue_on_failure=True,
#     # prevent_outside=True,
#     # base_url=None,
#     # ...
# )

loader = RecursiveUrlLoader(
    "https://docs.python.org/3.9/",
    prevent_outside=True,
    extractor=bs4_extractor,
    base_url="https://docs.python.org",
    link_regex=r'<a\s+(?:[^>]*?\s+)?href="([^"]*(?=index)[^"]*)"',
    exclude_dirs=['https://docs.python.org/3.9/faq']
)


docs = loader.load()

for doc in docs:
    print(doc)
 
