"""
chat_gpt_clone.py - a Chat-GPT like app
"""

import streamlit as st
from utils import apply_styles
from dotenv import load_dotenv
from openai import OpenAI

# load all API keys
load_dotenv()

# create my LLM
llm = OpenAI()

st.title("ChatGPT Clone")

if st.button("💬 New Chat"):
    # reset chat history
    st.session_state.messages = []
    st.rerun()

apply_styles()

if "messages" not in st.session_state:
    st.session_state.messages = []

# display all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What's up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = llm.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )
