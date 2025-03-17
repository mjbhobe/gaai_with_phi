"""
agent_with_memory_and_tools.py - adding web search capability (via tools) to
    our Q&A agent, with memory.

This example adds web search capability to the Q&A agent with memory, which we
coded in agent_with_memory.py. When you ask a question that the LLM cannot answer
from its pretrained knowledgebase, it will try and search the web to get additional
context that it can answer from. For websearch we'll use the DuckDuckGoTools.

As before, we'll be using Google Gemini 2.0 Flash as our LLM, but you can use any
supported LLM. The LLM is not yet equipped with any tools or additional knowledgebase
(such as that from RAG), so all responses are coming from it's pretrained knowledgebase.

We have added some Mumbai flair - the responses from the LLM will
be using Mumbai-lingo (you'll get an explanation of the slang, don't worry boss!)

@Author: Manish Bhobé
My experiments with Python, AI/ML and Generative AI
Code has been shared for learning purposes only! Use at own risk
"""

import os
from textwrap import dedent
from dotenv import load_dotenv, find_dotenv
from rich import print
from rich.console import Console
from rich.markdown import Markdown

from agno.agent import Agent, RunResponse
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
import google.generativeai as genai

# load all API keys from .env file
load_dotenv(find_dotenv())
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

console = Console()


my_agent = Agent(
    name="Basic Q&A Agent with history",
    # here you specify the model - we are using Google Gemini 2.0 Flash
    model=Gemini(id="gemini-2.0-flash-exp"),
    # the system message for this agent
    description=dedent(
        ## make it work like a local from Mumbai
        """
        - Think of yourself as an enthusiastic assistant, ready to help you with any questions you have.
        - You have deep knowledge about the world, and about Mumbai in particular.
        """
    ),
    # additional instructions, appended to system message
    instructions=dedent(
        """
        - You are a local from Mumbai, India, who is proficient in English as well as local slang.
        - Don't limit your responses to questions about Mumbai as your knowledge is NOT limited to Mumbai 
          alone. Answer any question from the user.
        - Use casual English in your response, but throw in Mumbai slang words (such as "fundu", "jugaad",
          "bawa", "bole to", "gyaan", "aapunki" etc.) - it will make you more relatable. Add a meaning of the Mumbai slang in brackets the first time you use it in a conversation, so non-Mumbai folks can
          understand aapunki bhaasha (slang for "our lingo").
        - Don't start all your responses with "Ayy" - use some variety, your responses need not always sound
          like a local "tapori" (slang for a "street thug").
        - Use all tools provided to you to fetch the latest information, if needed. Don't rely just on your tacit knowledge.
        - If you cannot answer a question, say so, and don't try to fake it. Apologize in classic Mumbai 
          style.
        """
    ),
    # debug_mode =True is used to show all the internal steps in terminal
    # VERY USEFUL to understand how the Agent is working
    debug_mode=True,
    # add previous chat history to messages
    # retain last 5 messages in memory
    add_history_to_messages=True,
    num_history_responses=5,
    # add our web search tools
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
)

user_prompt = None
while True:
    # infinite loop
    console.print("[cyan]What do you want to know:[/cyan]", end=" ")
    user_prompt = input()
    if user_prompt.strip().lower() in ["bye", "quit", "exit"]:
        break
    # my_agent.print_response(user_prompt)
    console.print("[yellow]Thinking...[/yellow]", end="")
    response: RunResponse = my_agent.run(user_prompt)
    console.print("\r", end="")
    console.print(Markdown(response.content))
