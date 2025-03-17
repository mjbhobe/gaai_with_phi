"""
basic_agent_streamlit.py - basic Q&A with an LLM via Agno (PhiData) Agent
    using a streamlit based UI.

This application illustrated basic Q&A with an LLM (we will use
Google Gemini 2.0 Flash in this example, but you can use any
supported LLM). The LLM does not maintain any "chat history" nor
any context from RAG, nor use any tools. So all responses are
coming from it's pretrained knowledgebase only.

We have added some Mumbai flair - the responses from the LLM will
be using Mumbai-lingo (you'll get an explanation of the slang, don't worry boss!)

@Author: Manish Bhobé
My experiments with Python, AI/ML and Generative AI
Code has been shared for learning purposes only! Use at own risk
"""

import streamlit as st
import os
from textwrap import dedent
from dotenv import load_dotenv, find_dotenv
from agno.agent import Agent, RunResponse
from agno.models.google import Gemini
import google.generativeai as genai

# Load environment variables and configure Gemini
load_dotenv(find_dotenv())
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Agent
my_agent = Agent(
    name="Basic Q&A Agent",
    model=Gemini(id="gemini-2.0-flash-exp"),
    description=dedent(
        """
        - Think of yourself as an enthusiastic assistant, ready to help you with any questions you have.
        - You have deep knowledge about the world, and about Mumbai in particular.
        """
    ),
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
        - Use any tools provided to you only if you cannot answer the question directly. Don't use tools for 
          every question.
        - If you cannot answer a question, say so, and don't try to fake it. Apologize in classic Mumbai 
          style.
        """
    ),
    debug_mode=False,  # Set to False in production
)

# Streamlit UI
st.title("Mumbai Local: Ask Anything!")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input for user question
question = st.expander("Ask your question here", expanded=True)
with question:
    user_input = st.text_area("Your Question", height=100)
    if st.button("Submit"):
        if user_input:
            # Get agent response
            response: RunResponse = my_agent.run(user_input)
            # agent_response = response.output

            # Update chat history
            st.session_state.chat_history.append(
                {"user": user_input, "agent": response.content}
            )

# Display chat history in a scrollable area
st.markdown("---")
st.subheader("Conversation")
chat_area = st.empty()  # Create an empty container to update the chat

if st.session_state.chat_history:
    chat_content = ""
    for chat in reversed(st.session_state.chat_history):
        # show most recent response first
        chat_content += f"**You:** {chat['user']}\n\n"
        chat_content += f"{chat['agent']}\n\n---\n\n"
    chat_area.markdown(chat_content)
else:
    chat_area.markdown("No conversation yet.")
