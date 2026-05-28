from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

# Client create
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("Simple Gemini Chatbot")
print("Type 'exit' to quit\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chat ended.")
        break

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_input
    )

    print("AI:", response.text)