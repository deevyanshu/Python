#directly calling the function without checking for function call in the response and then sending the result back to model for final response generation
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import requests

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client= genai.Client(api_key=GEMINI_API_KEY)

def get_current_weather(location:str,targetDate:str):
    """Get the current weather in a given location on given date"""

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

config=types.GenerateContentConfig(tools=[get_current_weather],service_tier="flex")

response=client.models.generate_content(
    model="gemini-3-flash-preview",
    config=config,
    contents="What's the temperature in Delhi on 2026-04-10?"
)

print(response.text) 