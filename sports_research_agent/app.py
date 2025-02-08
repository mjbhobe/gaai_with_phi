"""app.py - streamlit based front-end for application"""

import streamlit as st
from utils import apply_styles
from agents import agent, as_stream

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
        chunks = agent.run(prompt, stream=True)
        response = st.write_stream(as_stream(chunks))

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )
