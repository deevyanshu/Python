import logging
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
import os
import asyncio
from aiogram.filters import CommandStart

load_dotenv()

TELEGRAM_BOT_TOKEN= os.getenv("TELEGRAM_BOT_TOKEN")

#configure logging
logging.basicConfig(level=logging.INFO)

#initialize bot and dispatcher
bot=Bot(token=TELEGRAM_BOT_TOKEN)
dp=Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    """
    This handler responds to the /start and /help commands. 
    """
    await message.reply("Hello! I'm a Gemini-powered Telegram bot. Send me a message and I'll respond using the Gemini API!")

@dp.message()
async def echo(message: types.Message):
    """
    This will return echo
    """
    await message.answer(message.text)

async def main() -> None:
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
