"""
agents.py - define all the agents for the Sports Agent application

@Author: Manish Bhobe
My experiments with Python, AI/ML and Generative AI
Code has been shared for learning purposes only! Use at own risk
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.run.response import RunEvent, RunResponse

# load API keys from .env file
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    raise KeyError("GOOGLE_API_KEY is not defined in environment!")

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[DuckDuckGoTools(), Newspaper4kTools()],
    description="Researcher writing an article about a topic",
    instructions=[
        "For the given topic, search for the top 5 links.",
        "Then read each URL and extract the article text.",
        "Analyze and prepare 5-10 bullets about the topic based on the information extracted",
    ],
    markdown=True,
    show_tool_calls=True,
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    # where to store message histories?
    storage=SqliteAgentStorage(table_name="agent_sessions", db_file="./agent.db"),
)


def as_stream(response):
    for chunk in response:
        if isinstance(chunk, RunResponse) and isinstance(chunk.content, str):
            if chunk.event == RunEvent.run_response:
                yield chunk.content
