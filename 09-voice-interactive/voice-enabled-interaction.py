import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import pyttsx3
import speech_recognition as sr

# Load environment variables
load_dotenv()

# Initialize OpenAI models and components
embeddings = OpenAIEmbeddings()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
output_parser = StrOutputParser()

# Initialize text splitter with specified chunk size and overlap
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20, length_function=len, is_separator_regex=False)

# Load PDF using PyPDFLoader
loader = PyPDFLoader("myresume.pdf")
docs = loader.load_and_split(text_splitter)

# Create and save embeddings in Chroma database
db = Chroma.from_documents(docs, embedding=embeddings, persist_directory="my-rag")
retriever = db.as_retriever()

# Define chat prompts and chains for question answering
contextualize_q_system_prompt = "Given a chat history and the latest user question, formulate a standalone question. Do NOT answer the question."
contextualize_q_prompt = ChatPromptTemplate.from_messages([("system", contextualize_q_system_prompt), MessagesPlaceholder(variable_name="chat_history"), ("human", "{question}")])
question_chain = contextualize_q_prompt | llm | StrOutputParser()

system_prompt = "You are an assistant for question-answering tasks. Use the retrieved context to answer the question."
qa_prompt = ChatPromptTemplate.from_messages([("system", system_prompt), MessagesPlaceholder("chat_history"), ("human", "{question}")])

def contextualized_question(input: dict):
    return question_chain if input.get("chat_history") else input["question"]

retriver_chain = RunnablePassthrough.assign(context=contextualized_question | retriever)

# Set up the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('voice', "com.apple.eloquence.en-US.Grandpa")
engine.setProperty('volume', 1.0)
engine.setProperty('rate', 200)

# Set up the speech recognition engine
recognizer = sr.Recognizer()

def speak(text):
    print("Assistant: " + text)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        audio = recognizer.listen(source, phrase_time_limit=5)
        print("Listening...")
    try:
        text = recognizer.recognize_google(audio)
        return text
    except Exception as e:
        print("Error: " + str(e))
        return None

chat_history = []
speak("Hello, I am your assistant. How can I help you today?")

while True:
    prompt = listen()
    if prompt is not None:
        print("User: " + prompt)
        if prompt.lower() == 'exit':
            break

        ai_msg = retriver_chain.invoke({"question": prompt, "chat_history": chat_history})
        chat_history.extend([HumanMessage(content=prompt), ai_msg])

        speak(ai_msg['text'])
        print("*************************************************")
    else:
        speak("I'm sorry, I didn't understand that. Can you please repeat?")