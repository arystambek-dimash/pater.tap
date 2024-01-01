from telegram.ext import *
from dotenv import load_dotenv, get_key

load_dotenv()
API_KEY = get_key("./", "TELEGRAM_BOT_API", "utf-8")

if __name__ == "__main__":
    updater = Updater(API_KEY)
    dp = updater.dis
