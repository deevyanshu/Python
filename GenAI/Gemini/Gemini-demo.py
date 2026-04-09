import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client= genai.Client(api_key=GEMINI_API_KEY)

# response = client.models.generate_content(
#     model="gemini-3-flash-preview",
#     contents="hello"
# )

# response = client.models.generate_content(
#     model="gemini-3-flash-preview",
#     config={
#         'system_instruction': "You are an expert Java developer with 20 years of experience. Answer concisely.",
#         'service_tier': 'flex'
#         },
#     contents="How do I implement a custom OAuth2 filter in Spring Boot?"
# )


# print(response.text)

# response = client.models.generate_content_stream(
#     model="gemini-3-flash-preview",
#     config={
#         'system_instruction': "You are an expert Java developer with 20 years of experience. Answer concisely.",
#         'service_tier': 'flex'
#         },
#     contents="How do I implement a custom OAuth2 filter in Spring Boot?"
# )

# for chunk in response:
#     print(chunk.text, end="", flush=True)

#chat history or Multi-turn conversations
chat= client.chats.create(model="gemini-3-flash-preview",
config={'service_tier': 'flex',
        'max_output_tokens': 100}
) #create the stateful chat session

response = chat.send_message("Hi my name is deevyanshu") #first turn
print(f"AI: {response.text}")

response = chat.send_message("What is my name?") #second turn, the model should remember the context from the first turn
print(f"AI: {response.text}")
