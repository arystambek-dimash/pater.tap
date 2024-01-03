from aiogram import F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton, CallbackQuery
)
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from . import router
from .utils import get_user_by_id
from ugc.models import TelegramUserSettings
from .states import DistanceForm
from .utils import edit_message_text


@router.message(Command("menu"))
async def language_handler(msg: Message):
    user = await get_user_by_id(msg.from_user.id)
    menu_text = ""
    await msg.answer("Тілді таңдаңыз / Выберите язык:", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Русский 🇷🇺", callback_data='Ru'),
         InlineKeyboardButton(text="Қазақ 🇰🇿", callback_data='Kz')]
    ]))


@router.callback_query(lambda c: c.data in ('Ru', 'Kz'))
async def process_callback(callback_query: CallbackQuery):
    language = 'rus' if callback_query.data == 'Ru' else 'kaz'
    await change_language(language, callback_query)
