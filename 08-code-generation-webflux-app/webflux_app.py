import streamlit as st
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from dotenv import load_dotenv
import argparse

load_dotenv()

st.title("Code and TestCase Generation Tool")

# parser=argparse.ArgumentParser()
# parser.add_argument("--task",default="return a list of prime numbers from 1 to 50")
# parser.add_argument("--language", default="java")
# args=parser.parse_args()

llm = OpenAI()

language = st.text_input("Enter the programming language")
task=  st.text_input("What code you want to generate today?")

code_prompt=PromptTemplate(
    template="write a very short {language} function that will {task}",
    input_variables=["language", "task"]
)

test_prompt=PromptTemplate(
    input_variables=["language","code"],
    template="write a test for the following {language} code:\n{code}"

)



code_chain=LLMChain(
    llm=llm,
    prompt=code_prompt,
    output_key= "code"
)

test_chain=LLMChain(
    llm=llm,
    prompt=test_prompt,
    output_key="test"


)

chain=SequentialChain(
   chains=[code_chain,test_chain],
   input_variables=["task","language"],
   output_variables=["code","test"]
)

# result=chain({
#     "language" : {args.language},
#     "task": args.task
# })

result=chain({
    "language" : {language},
    "task": {task}
})


print(">>>>>>>>>>>>>>>>>>>>")
print(result["code"])
print(">>>>>>>>>>>>>>>>>>>>>")
print(result["test"])

st.write(">>>>>>>>>>>>>>>>>>>>>")
st.write("The code is")
st.write(result["code"])

st.write(">>>>>>>>>>>>>>>>>>>>>")
st.write("The test case for the above code snippet is ")
st.write(result["test"])

