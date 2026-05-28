
from google import genai
from dotenv import load_dotenv
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain_core.prompts import ChatPromptTemplate
from colorama import Fore, Style, init
import os

# Initialize Colorama
init(autoreset=True)

# Load env
load_dotenv()

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

print(Fore.CYAN + "\n🤖 Gemini CLI Chatbot")
print(Fore.YELLOW + "Type 'exit' to quit\n")

# Chat Memory
chat_history = []

# System Prompt
system_message = SystemMessage(
    content="""
You are a helpful AI assistant.
Reply in a smart and concise way.
"""
)

while True:

    user_input = input(
        Fore.GREEN + "You: " + Style.RESET_ALL
    )

    if user_input.lower() == "exit":
        print(Fore.RED + "Chat ended.")
        break

    # Human Message
    human_message = HumanMessage(content=user_input)
    chat_history.append(human_message)

    # Prompt Template
    prompt = ChatPromptTemplate.from_messages(
        [system_message] + chat_history
    )

    formatted_messages = prompt.format_messages()

    # Convert Messages
    final_prompt = ""

    for msg in formatted_messages:

        if isinstance(msg, SystemMessage):
            final_prompt += f"System: {msg.content}\n"

        elif isinstance(msg, HumanMessage):
            final_prompt += f"Human: {msg.content}\n"

        elif isinstance(msg, AIMessage):
            final_prompt += f"AI: {msg.content}\n"

    print(Fore.BLUE + "\nAI: ", end="")

    streamed_text = ""

    # Streaming Response
    response_stream = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=final_prompt
    )

    for chunk in response_stream:

        if chunk.text:
            print(chunk.text, end="", flush=True)
            streamed_text += chunk.text

    print("\n")

    # Save AI Message
    chat_history.append(
        AIMessage(content=streamed_text)
    )
