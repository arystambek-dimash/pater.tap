import asyncio
import os

import django
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    KeyboardButton,
    ReplyKeyboardMarkup, ReplyKeyboardRemove,
)
from django.core.exceptions import ObjectDoesNotExist

from ugc.models import TelegramUser

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rest.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

router = Router()


async def edit_message_text(message, text):
    await message.edit_text(text)


async def change_language(language, callback_query=None):
    user_id = callback_query.from_user.id if callback_query else None
    username = callback_query.from_user.username if callback_query else None

    user, created = await get_or_create_user(user_id, username, language)

    first_name = callback_query.from_user.first_name
    confirmation_message = {
        "rus": f"Язык изменен на 🇷🇺 русский язык для пользователя {first_name}.",
        "kaz": f"Тіл 🇰🇿 қазақ тіліне өзгерді, пайдаланушы {first_name} үшін.",
    }[language] if created else {
        "rus": f"Русский язык установлен для пользователя {first_name}.",
        "kaz": f"Қазақ тілі пайдаланушы {first_name} үшін орнатылды.",
    }[language]

    await edit_message_text(callback_query.message, confirmation_message)
    if user.tg_user_lang == "rus":
        location_km_text = "Теперь укажите расстояние, на которое вы хотите искать жилье (от 5 до 80)"
        expires_time = "Время ожидания истекло. Пожалуйста, повторите команду."
        isdigit_exception = "Пожалуйста, введите целое число."
        skip_text = "Пропустить"
        distance_text_error = "Чтобы задать расстояние, введите /distance"
    else:
        location_km_text = "Енді жазыңыз, қанағаттану іздеуіңіздің қашықтығын көрсетіңіз (5-тен 80-ге дейін)"
        expires_time = "Күту уақыты аяқталды. Пәрменді қайталаңыз."
        isdigit_exception = "Бүтін санды енгізіңіз."
        skip_text = "Өткізіп жіберу"
        distance_text_error = "Қашықтықты орнату үшін /қашықтықты енгізіңіз"
    try:
        response = await callback_query.message.answer(location_km_text)
        await response.message.answer(skip_text, reply_markup=ReplyKeyboardRemove())
        response = await callback_query.message.await_message(timeout=10)
        if response.text.lower() == skip_text.lower():
            pass
        elif response.text.isdigit():
            get_km = int(response.text)
            if 5 <= get_km <= 80:
                user.location_km = get_km
            else:
                await callback_query.message.answer(distance_text_error)
        else:
            await callback_query.message.answer(isdigit_exception)
            await callback_query.message.answer(distance_text_error)
    except asyncio.TimeoutError:
        await callback_query.message.answer(expires_time)


async def get_or_create_user(user_id, username, language):
    return TelegramUser.objects.get_or_create(
        tg_user_id=user_id,
        defaults={"tg_username": username, "tg_user_lang": language},
    )


async def get_user_by_id(user_id):
    try:
        return TelegramUser.objects.get(tg_user_id=user_id)
    except ObjectDoesNotExist:
        return None


keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Русский 🇷🇺", callback_data='Ru'),
     InlineKeyboardButton(text="Қазақ 🇰🇿", callback_data='Kz')]
])


@router.message(Command("start"))
async def start_handler(msg: Message):
    user = await get_user_by_id(msg.from_user.id)
    if not user:
        await msg.answer(
            "Қош келдіңіз! Тілді таңдаңыз / Добро пожаловать! Пожалуйста, выберите язык",
            reply_markup=keyboard,
        )
    else:
        await msg.answer("Қайта қош келдіңіз! / Добро пожаловать!")


@router.callback_query(lambda c: c.data in ('Ru', 'Kz'))
async def process_callback(callback_query: CallbackQuery):
    language = 'rus' if callback_query.data == 'Ru' else 'kaz'
    await change_language(language, callback_query)


@router.message(Command("language"))
async def language_handler(msg: Message):
    await msg.answer("Тілді таңдаңыз / Выберите язык:", reply_markup=keyboard)
