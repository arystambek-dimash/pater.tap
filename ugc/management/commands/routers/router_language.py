from . import router
from aiogram.types import InlineKeyboardMarkup, \
    InlineKeyboardButton, \
    CallbackQuery
from aiogram.filters import Command
from aiogram.types import Message

from .utils import change_language


@router.message(Command("language"))
async def language_handler(msg: Message):
    await msg.answer("Тілді таңдаңыз / Выберите язык:", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Русский 🇷🇺", callback_data='Ru'),
         InlineKeyboardButton(text="Қазақ 🇰🇿", callback_data='Kz')]
    ]))


@router.callback_query(lambda c: c.data in ('Ru', 'Kz'))
async def process_callback(callback_query: CallbackQuery):
    language = 'rus' if callback_query.data == 'Ru' else 'kaz'
    await change_language(language, callback_query)
