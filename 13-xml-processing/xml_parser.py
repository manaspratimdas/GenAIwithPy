from bs4 import BeautifulSoup
import json
import xmltodict
from langchain.agents import create_json_agent
from langchain.agents.agent_toolkits import JsonToolkit
from langchain.tools.json.tool import JsonSpec
from langchain_openai import ChatOpenAI


with open(r"HelloWorld.xml","r") as f1:
    content=f1.read()
text_content=str(BeautifulSoup(content,"lxml"))
# clreprint(text_content)
xml_dict=xmltodict.parse(text_content)
spec=JsonSpec(dict_=xml_dict)
print(spec)
# toolkit=JsonToolkit(spec=spec)
# agent=create_json_agent(llm=ChatOpenAI(temperature=0,model="gpt-4o"),toolkit=toolkit,max_iterations=3000,verbose=True)

# question="""
# You are a integration specialist. You are required review content for the functionality and  convert the below code that is derived from the mulesoft xml file to pseudo code. 
# You will be using this pseudo code to write program
# """

# response=agent.run(question)
# print(response)