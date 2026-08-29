from langchain.agents import create_agent
from langchain_groq import ChatGroq
from src.tools.tools import web_search,scrape_webpage
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGroq(
    model='openai/gpt-oss-20b',
    temperature=0,
    max_tokens=2048,
    reasoning_effort="low"   
)

def search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

def reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_webpage],
    )


writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert at writing research. Write the topic in a well-structured, well-organized way."),
    ("human", "Write a detailed research report on this topic.\n\nTopic: {topic}\n\nResearch Gathered:\n{research}")
])
writer_chain = writer_prompt | llm | StrOutputParser()

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", "Review the research report below and evaluate it strictly.\n\nReport:\n{report}")
])
critic_chain = critic_prompt | llm | StrOutputParser()
