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


@router.message(Command("settings"))
async def user_settings(msg: Message):
    user = await get_user_by_id(msg.from_user.id)
    try:
        user_setting = TelegramUserSettings.objects.get(telegram_user__user_id=msg.from_user.id).user_distance
    except TelegramUserSettings.DoesNotExist:
        user_setting = None
    distance_text = "Қашықтық қою" if user.lang == "kaz" else "Задать дистанцию"
    delete_user_data_text = "Қолданушы деректерін жою" if user.lang == "kaz" else "Удалить персональные данные"
    choose_text = "Тармақтардын бірін таңдаңыз" if user.lang == "kaz" else "Выберите один из пунктов"
    if user_setting:
        distance_text = "Қашықтықты озгерту" if user.lang == "kaz" else "Изменить дистанцию"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=distance_text, callback_data='distance')],
        [InlineKeyboardButton(text=delete_user_data_text, callback_data='delete')],
    ])
    await msg.answer(text=choose_text, reply_markup=kb)


@router.callback_query(lambda c: c.data == "distance")
async def set_distance(query: CallbackQuery, state: FSMContext):
    user = await get_user_by_id(query.from_user.id)
    try:
        user_setting = TelegramUserSettings.objects.get(telegram_user=user)
    except TelegramUserSettings.DoesNotExist:
        user_setting = None
    if not user_setting:
        set_distance_text = "Сіз қандай қашықтықты орнатқыңыз келеді?" if user.lang == "kaz" else "Какое расстояние вы хотите установить?"
    else:
        set_distance_text = f"Ағымдағы қашықтық {user_setting.user_distance}км, қандай қашықтықты орнатқыңыз келеді?" if user.lang == "kaz" else f"Ваше текущее расстояние {user_setting.user_distance} км, какое расстояние вы хотите установить?"
    await edit_message_text(query.message, set_distance_text)
    await state.set_state(DistanceForm.GET_DISTANCE)


@router.message(StateFilter(DistanceForm.GET_DISTANCE), F.text)
async def process_distance(message: Message, state: FSMContext):
    user = await get_user_by_id(message.from_user.id)
    try:
        user_setting = TelegramUserSettings.objects.get(telegram_user=user)
    except TelegramUserSettings.DoesNotExist:
        user_setting = None
    if not user_setting:
        distance_text = "Сіз {distance} км орнатыңыз" if user.lang == "kaz" else "Вы установили {distance} км"
        try:
            value = int(message.text)
            if 1 <= value <= 30:
                await state.update_data(GET_DISTANCE=value)
                TelegramUserSettings.objects.create(user_distance=value, telegram_user=user)
                await state.clear()
                await message.answer(distance_text.format(distance=value))
            else:
                raise ValueError
        except ValueError:
            exception_text = "Қашықтық тек сандар болуы керек және ол 1 ден 30 км аралығында болуы керек" if user.lang == "kaz" else "Расстояние должно быть только цифрами и это должно быть от 1 до 30 км"
            await message.answer(exception_text)
    else:
        prev_distance = user_setting.user_distance
        distance_text = "Қашықтық {} км ден -> {} км ге озгерды" if user.lang == "kaz" else "Расстояние изменился от {} км -> до {} км"
        try:
            value = int(message.text)
            if 1 <= value <= 30:
                await state.update_data(GET_DISTANCE=value)
                user_setting.user_distance = value
                await state.clear()
                await message.answer(distance_text.format(prev_distance, value))
            else:
                raise ValueError
        except ValueError:
            exception_text = "Қашықтық тек сандар болуы керек және ол 1 ден 30 км аралығында болуы керек" if user.lang == "kaz" else "Расстояние должно быть только цифрами и это должно быть от 1 до 30 км"
            await message.answer(exception_text)


@router.callback_query(lambda c: c.data == "delete")
async def delete_user_data(query: CallbackQuery):
    user = await get_user_by_id(query.from_user.id)
    delete_text = "Вы точно хотите удалить данные?" if user.lang == "rus" else "Сіз деректерді жойғыңыз келе ме?"
    yes = "Да" if user.lang == "rus" else "Ия"
    no = "Нет" if user.lang == "rus" else "Жок"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=yes, callback_data='yes'),
         InlineKeyboardButton(text=no, callback_data='no')],
    ])
    await query.message.edit_text(delete_text, reply_markup=kb)


@router.callback_query(lambda c: c.data == "yes")
async def confirm_delete_yes(query: CallbackQuery):
    user = await get_user_by_id(query.from_user.id)
    user.delete()
    await query.message.edit_text(
        "Данные успешно удалены. Чтобы начать заново кликай --> /start" if user.lang == "rus" else "Деректер сәтті өшірілді. Қайта бастау үшін басыңыз --> /start")


@router.callback_query(lambda c: c.data == "no")
async def confirm_delete_no(query: CallbackQuery):
    user = await get_user_by_id(query.from_user.id)
    await query.message.edit_text("Отменено." if user.lang == "rus" else "Бас тартылды.")
