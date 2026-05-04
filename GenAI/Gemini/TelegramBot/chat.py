from dotenv import load_dotenv
import os
from aiogram import types, Dispatcher, Bot
from google import genai
from aiogram.filters import CommandStart, Command
import asyncio

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

TELEGRAM_BOT_TOKEN= os.getenv("TELEGRAM_BOT_TOKEN")

class Reference:
    '''
    A class to store previously response from the Gemini API
    '''
    def __init__(self)-> None:
        self.reference= ""

referenceObj=Reference()
model_name="gemini-3-flash-preview"
client=genai.Client(api_key=GEMINI_API_KEY)

bot=Bot(token=TELEGRAM_BOT_TOKEN)
dp=Dispatcher()

def clear_past():
    """
    Clear the past conversation
    """
    referenceObj.reference= ""

@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    """
    This handler responds to the /start and /help commands. 
    """
    await message.reply("Hello! I'm a Gemini-powered Telegram bot. Send me a message and I'll respond using the Gemini API!")

@dp.message(Command("help"))
async def helper(message: types.Message):
    """
    This handler responds to the /help command. 
    """
    help_command="""
    Here are the available commands:
    /start - to start the conversation
    /clear - to clear the conversation
    /help - to show this help message
    """

    await message.reply(help_command)

@dp.message(Command("clear"))
async def clear(message: types.Message):
    """
    This handler responds to the /clear command. It will clear the past conversation
    """
    clear_past()
    await message.reply("Conversation cleared!")

@dp.message()
async def gemini(message: types.Message):
    """
    A handler to process the user's input and generate a response using gemini
    """

    response=client.models.generate_content(
        model=model_name,
        contents=[
            {
                "role":"model",
                "parts": [{"text":referenceObj.reference}]
            },
            {
                "role":"user",
                "parts": [{"text":message.text}]
            }
        ],
        config={
            'service_tier': 'flex'
        }
    )

    if response.text:
        referenceObj.reference = response.text
        print(f"gemini: {referenceObj.reference}")
        await bot.send_message(chat_id=message.chat.id, text=referenceObj.reference)
    else:
        # Handle safety blocks or empty responses
        print("Gemini returned empty. Check finish_reason:", response.candidates[0].finish_reason)
        await bot.send_message(chat_id=message.chat.id, text="I'm sorry, I couldn't generate a reply.")

async def main() -> None:
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())