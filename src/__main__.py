import os 
import logging 
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from src.handlers.user_handlers import register_user_handlers

from src.runners.webhook import WebhookRunner
from src.runners.polling import PollingRunner

load_dotenv()

def register_handlers(dp) -> None:  
    register_user_handlers(dp)

  
def main() -> None:   
    TOKEN = os.getenv("TOKEN")  
    PROJECT_ROOT = os.getenv("PROJECT_ROOT")
    RUN_MODE = os.getenv("RUN_MODE")

    dp = Dispatcher()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    register_handlers(dp)    
    if RUN_MODE == 'polling': 
        runner = PollingRunner(bot, dp)
    elif RUN_MODE == 'webhook':         
        runner = WebhookRunner(bot, dp)
    else:
        raise ValueError('Invalid RUN_MODE env variable')
    
    runner.run()


if __name__ == "__main__":
    main()