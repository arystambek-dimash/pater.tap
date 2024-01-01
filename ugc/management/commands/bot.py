from django.core.management.base import BaseCommand
from django.conf import settings
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode

from ugc.management.commands.router import router


class Command(BaseCommand):
    help = "Telegram bot"

    def handle(self, *args, **options):
        bot = Bot(token=settings.TOKEN, parse_mode=ParseMode.HTML)
        dp = Dispatcher()
        dp.include_router(router=router)
        dp.run_polling(bot)
