from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.filters import Command

from . import router
from .utils import get_user_by_id


@router.message(Command("start"))
async def start_handler(msg: Message):
    user = await get_user_by_id(msg.from_user.id)
    if not user:
        await msg.answer(
            "Қош келдіңіз! Тілді таңдаңыз / Добро пожаловать! Пожалуйста, выберите язык",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Русский 🇷🇺", callback_data='Ru'),
                 InlineKeyboardButton(text="Қазақ 🇰🇿", callback_data='Kz')]
            ]),
        )
    else:
        if user.lang == "rus":
            await msg.answer(f"Добро пожаловать! {user.username}")
        else:
            await msg.answer(f"Қайта қош келдіңіз! {user.username}")
