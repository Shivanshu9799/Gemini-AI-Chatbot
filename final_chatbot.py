from google import genai
from dotenv import load_dotenv
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain_core.prompts import ChatPromptTemplate
import os

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("Simple Gemini Chatbot with History")
print("Type 'exit' to quit\n")

# Store chat history
chat_history = []

# System message
system_message = SystemMessage(
    content="You are a helpful AI assistant."
)

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chat ended.")
        break

    # Human message
    human_message = HumanMessage(content=user_input)

    # Add user message to history
    chat_history.append(human_message)

    # Create prompt template
    prompt = ChatPromptTemplate.from_messages(
        [system_message] + chat_history
    )

    # Format messages
    formatted_messages = prompt.format_messages()

    # Convert messages into plain text for Gemini
    final_prompt = ""

    for msg in formatted_messages:
        if isinstance(msg, SystemMessage):
            final_prompt += f"System: {msg.content}\n"

        elif isinstance(msg, HumanMessage):
            final_prompt += f"Human: {msg.content}\n"

        elif isinstance(msg, AIMessage):
            final_prompt += f"AI: {msg.content}\n"

    # Generate response
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=final_prompt
    )

    ai_text = response.text

    # AI message
    ai_message = AIMessage(content=ai_text)

    # Save AI response to history
    chat_history.append(ai_message)

    # Print AI response
    print("AI:", ai_text)