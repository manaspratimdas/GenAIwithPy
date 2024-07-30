from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
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


code_chain=LLMChain(
    llm=llm,
    prompt=code_prompt,
    output_key= "code"

)

result=code_chain({
    "language" : args.language,
    "task": args.task
})



print(">>>>>>>>>>>>>>>>>>>>")
print(result["task"])


print(">>>>>>>>>>>>>>>>>>>>>")
print(result["code"])