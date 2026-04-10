#This approach for more better control on function calling for specific custom workflow
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import requests

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client= genai.Client(api_key=GEMINI_API_KEY)

def get_current_weather(location,targetDate):
    """Get the current weather in a given location"""

    url="https://ai-weather-by-meteosource.p.rapidapi.com/time_machine"

    querystring= {
        "place_id":location,
        "date": targetDate
    }

    headers = {
	"x-rapidapi-key": "9d01bdfe74msh4606261d5e9c83ap194472jsn37fff811dd1b",
	"x-rapidapi-host": "ai-weather-by-meteosource.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    # print(response.json())

    return response.json()

# response = get_current_weather("Delhi","2026-04-10")

# Define the function declaration for the model
weather_function={
    "name":"get_current_weather",
    "description":"Get the current weather in a given location",
    "parameters":{
        "type":"object",
        "properties":{
            "location":{
                "type":"string",
                "description":"The city , e.g. San Francisco"
            },
            "targetDate":{
                "type":"string",
                "description":"The date to get the weather for, in YYYY-MM-DD format"
            }
        },
        "required":["location","targetDate"]
    }
}

# Configure the client and tools

tools=types.Tool(function_declarations=[weather_function])
config=types.GenerateContentConfig(tools=[tools],service_tier="flex")

#define user prompt
contents = [
    types.Content(
        role="user", parts=[types.Part(text="What's the temperature in Delhi on 2026-04-10?")]
    )
]

# Send request with function declarations
response=client.models.generate_content(
    model="gemini-3-flash-preview",
    config=config,
    contents=contents
)

# Check for a function call
# print(response)
if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call
    print(f"Function to call: {function_call.name}")
    print(f"ID: {function_call.id}")
    print(f"Arguments: {function_call.args}")
    print(f"response: {response}")
    #  In a real app, you would call your function here:
    result = get_current_weather(**function_call.args)
    # print(f"Function result: {result}")
    
    # Create a function response part
    function_response_part = types.Part.from_function_response(
        name=function_call.name,
        response={"result": result},
        
    )

    # Append function call and result of the function execution to contents
    contents.append(response.candidates[0].content) # Append the content from the model's response.
    contents.append(types.Content(role="user",parts=[function_response_part])) # Append the function response
    final_response= client.models.generate_content(
        model="gemini-3-flash-preview",
        config=config,
        contents=contents
    )
    print(final_response.text)
else:
    print("No function call found in the response.")
    print(response.text)