import streamlit as st
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import argparse

load_dotenv()

# parser=argparse.ArgumentParser()
# parser.add_argument("--task",default="return a list of prine numbers from 1 to 100")
# parser.add_argument("--language", default="java")
# args=parser.parse_args()



llm = OpenAI()

# code_prompt=PromptTemplate(
#     template="write a very short {language} function that will {task}",
#     input_variables=["language", "task"]
# )


# code_chain=LLMChain(
#     llm=llm,
#     prompt=code_prompt,
#     output_key= "code"

# )

# result=code_chain({
#     "language" : args.language,
#     "task": args.task
# })

# language = input(">> ")
# task= input(">> ")
st.title("GenAI intro")

language = st.text_input(" Enter the language")
task=  st.text_input("Summary of the task that code snippet should do")

template="""
As a Java developer, I require assistance in setting controller, service and repository layer for
 the spring boot webflux application created in the previos step.
  I am only looking for thr CURD procesing i the controller. 
  Include the maven plugin in the pom ensure that this project is setup for the spring reactive. 
  would appreciate a detailed, step-by-step guide to complete this task.
"""

code_prompt=PromptTemplate(
    # template="write a very short {language} function that will {task}. Display the result with proper formatting ",
    template=template,
    input_variables=["language", "task"]
)

code_chain=LLMChain(
    llm=llm,
    prompt=code_prompt,
    output_key= "code"

)

result=code_chain({
    "language" : {language},
    "task": {task}
})






print(">>>>>>>>>>>>>>>>>>>>")
print(result["task"])

st.write("The task is")
st.write(result["task"])


print(">>>>>>>>>>>>>>>>>>>>>")
print(result["code"])

st.write("The code")
st.write(result["code"])