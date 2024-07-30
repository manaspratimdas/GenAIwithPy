from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from dotenv import load_dotenv
import argparse

load_dotenv()

parser=argparse.ArgumentParser()
parser.add_argument("--task",default="return a list of numbers")
parser.add_argument("--language", default="java")
args=parser.parse_args()

llm = OpenAI()

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

result=chain({
    "language" : args.language,
    "task": args.task
})


print(">>>>>>>>>>>>>>>>>>>>")
print(result["code"])


print(">>>>>>>>>>>>>>>>>>>>>")
print(result["test"])