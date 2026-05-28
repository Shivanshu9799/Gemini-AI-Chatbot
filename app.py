
import streamlit as st
from google import genai
from dotenv import load_dotenv
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain_core.prompts import ChatPromptTemplate
import os

# Load env
load_dotenv()

# Gemini Client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Streamlit Page
st.set_page_config(page_title="Gemini AI Chatbot", page_icon="🤖")

st.title("🤖 Gemini AI Assistant")

# Session Memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# System Prompt
system_message = SystemMessage(
    content="""
You are a smart, helpful AI assistant.
Give concise and useful answers.
"""
)

# Display previous messages
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)

    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# User Input
user_input = st.chat_input("Type your message...")

if user_input:

    # Show User Message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Add Human Message
    human_message = HumanMessage(content=user_input)
    st.session_state.chat_history.append(human_message)

    # Prompt Template
    prompt = ChatPromptTemplate.from_messages(
        [system_message] + st.session_state.chat_history
    )

    formatted_messages = prompt.format_messages()

    # Convert to Gemini Text Prompt
    final_prompt = ""

    for msg in formatted_messages:

        if isinstance(msg, SystemMessage):
            final_prompt += f"System: {msg.content}\n"

        elif isinstance(msg, HumanMessage):
            final_prompt += f"Human: {msg.content}\n"

        elif isinstance(msg, AIMessage):
            final_prompt += f"AI: {msg.content}\n"

    # Assistant Message Box
    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        streamed_text = ""

        # Streaming Response
        response_stream = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=final_prompt
        )

        for chunk in response_stream:

            if chunk.text:
                streamed_text += chunk.text
                response_placeholder.markdown(streamed_text)

    # Save AI Message
    st.session_state.chat_history.append(
        AIMessage(content=streamed_text)
    )
