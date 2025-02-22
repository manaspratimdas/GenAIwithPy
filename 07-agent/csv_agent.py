import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent, create_csv_agent
from dotenv import load_dotenv
import pandas as pd


load_dotenv()

llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

output_parser =StrOutputParser()


st.title("AI Agent with LangChain")

df=pd.read_csv('customers.csv').fillna(value=0)

# print(df.head())

st.write(df.head())

agent=create_pandas_dataframe_agent(
    llm=llm,
    df=df,
    allow_dangerous_code=True,
    verbose=True
)

CSV_PROMPT_PREFIX="""
First set the pandas display the options to show all the columns,
get the column names, then answer the question
"""

CSV_PROMPT_SUFFIX="""
-**ALWAYS** before giving the final answer, try another method. 
Then reflect on the answers of the two methods you did and ask yourself
if it answers correctly the original question.
If you are not sure, try another method.
- If the methonds tried do not give the same result, reflect and try again until
you have two methods that have the same result.
-if you still cannot arrive to a consistent result, say that you are not sure
of the answer
- if you are sure of the correct answer, create a beautiful and through response
and through resoponse using markdown
- **DO NOT MAKE UP AN ANSWER OR USE PRIOR KNOWLEDGE,
ONLY USE THE RESULT OF THE CALCULATION YOU HAVE DONE**.
-**ALWAYS** as a part of the "final answer", explain how you got the result on a section that
start with "Explaination: ". In the explaination mention the column names that you have used
to get the answer
"""

CSV_ANSWER_FORMAT="""
Present the answer in the columnar format
"""

st.write("### Ask a question")

QUESTION=st.text_input(   
    "enter the question about the dataset"
    #  "list the top 5 countries which has maximum customer in descending order"
              )




if st.button("Run Query"):
    Query=CSV_PROMPT_PREFIX + QUESTION  + CSV_ANSWER_FORMAT
    result=agent.invoke(Query)
    st.write("### Final Answer")
    st.markdown(result["output"])


# print(result["output"])