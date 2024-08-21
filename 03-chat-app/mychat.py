from langchain_community.chat_models import ChatOpenAI
from  langchain.chains import LLMChain
from langchain.prompts import MessagesPlaceholder,HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv


load_dotenv

chat=ChatOpenAI()

memory=ConversationBufferMemory(memory_key="messages", return_messages=True)

prompt=ChatPromptTemplate(
    input_variables =["content","messages"],
     messages=[
         MessagesPlaceholder(variable_name="messages"),
         HumanMessagePromptTemplate.from_template("{content}")
    ]

)

chain=LLMChain(
    llm=chat,
    prompt=prompt,
    memory=memory
)

while True:
    content = input(">> ")
    
    if content.lower() in ["exit", "quit"]:
        print("Exiting chat.")
        break

    try:
        result = chain({"content": content})
        print(result["text"])
    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally, add a break or continue depending on the desired behavior after an error

