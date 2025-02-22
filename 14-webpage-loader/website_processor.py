from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://manaspratimdas.blogspot.com")

loader.requests_kwargs = {'verify':False}

docs = loader.load()

docs[0]

# print(docs[0].metadata)

# print(">>>>>>>>>>>>>>>>>>>>>>>>>")

# print(docs[0])
# print(">>>>>>>>>>>>>>>>>>>>>>>>>")

with open("website.txt", "w", encoding='utf-8') as file:
    file.write(f"Question: {docs[0]}\n")