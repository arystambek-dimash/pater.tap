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


async def get_user_setting(user_id):
    try:
        return TelegramUserSettings.objects.get(telegram_user__user_id=user_id).user_distance
    except TelegramUserSettings.DoesNotExist:
        return None


async def settings_handler(msg, msg_id=None):
    user = await get_user_by_id(msg.from_user.id)
    user_setting = await get_user_setting(msg.from_user.id)

    distance_text = "Қашықтық қою" if user.lang == "kaz" else "Задать дистанцию"
    delete_user_data_text = "Қолданушы деректерін жою" if user.lang == "kaz" else "Удалить персональные данные"
    choose_text = "Тармақтардын бірін таңдаңыз" if user.lang == "kaz" else "Выберите один из пунктов"

    if user_setting:
        distance_text = "Қашықтықты озгерту" if user.lang == "kaz" else "Изменить дистанцию"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=distance_text, callback_data='distance')],
        [InlineKeyboardButton(text=delete_user_data_text, callback_data='delete')],
    ])
    try:
        if not msg_id:
            await msg.answer(text=choose_text, reply_markup=kb)
        else:
            await msg.edit_text(text=choose_text, inline_message_id=msg_id, reply_markup=kb)
    except Exception as e:
        print(e)


@router.message(Command("settings"))
async def user_settings(msg: Message):
    await settings_handler(msg)


@router.callback_query(lambda c: c.data == "back_to_params")
async def user_back_to_params(query: CallbackQuery):
    await settings_handler(query.message, msg_id=query.message.message_id)


@router.callback_query(lambda c: c.data == "distance")
async def set_distance(query: CallbackQuery, state: FSMContext):
    user = await get_user_by_id(query.from_user.id)
    user_setting = await get_user_setting(query.from_user.id)

    set_distance_text = (
        "Сіз қандай қашықтықты орнатқыңыз келеді?" if user.lang == "kaz" else
        "Какое расстояние вы хотите установить?"
    ) if not user_setting else (
        f"Ағымдағы қашықтық {user_setting} км, қандай қашықтықты орнатқыңыз келеді?" if user.lang == "kaz" else
        f"Ваше текущее расстояние {user_setting} км, какое расстояние вы хотите установить?"
    )

    await edit_message_text(query.message, set_distance_text)
    await state.set_state(DistanceForm.GET_DISTANCE)


@router.message(StateFilter(DistanceForm.GET_DISTANCE), F.text)
async def process_distance(message: Message, state: FSMContext):
    user = await get_user_by_id(message.from_user.id)
    user_setting = await get_user_setting(message.from_user.id)

    distance_text = (
        "Сіз {distance} км орнатыңыз" if user.lang == "kaz" else
        "Вы установили {distance} км"
    )

    try:
        value = int(message.text)
        if 1 <= value <= 30:
            await state.update_data(GET_DISTANCE=value)
            if not user_setting:
                TelegramUserSettings.objects.create(user_distance=value, telegram_user=user)
            else:
                user_setting.user_distance = value
            await state.clear()
            await message.answer(distance_text.format(distance=value))
        else:
            raise ValueError
    except ValueError:
        exception_text = (
            "Қашықтық тек сандар болуы керек және ол 1 ден 30 км аралығында болуы керек" if user.lang == "kaz" else
            "Расстояние должно быть только цифрами и это должно быть от 1 до 30 км"
        )
        await message.answer(exception_text)


@router.callback_query(lambda c: c.data == "delete")
async def delete_user_data(query: CallbackQuery):
    user = await get_user_by_id(query.from_user.id)
    delete_text = (
        "Вы точно хотите удалить данные?" if user.lang == "rus" else
        "Сіз деректерді жойғыңыз келе ме?"
    )
    yes = "Да" if user.lang == "rus" else "Ия"
    no = "Нет" if user.lang == "rus" else "Жок"
    back_to_menu_text = "Параметрлерге қайту" if user.lang == "kaz" else "Назад к параметорам"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=yes, callback_data='yes'),
         InlineKeyboardButton(text=no, callback_data='no')],
        [InlineKeyboardButton(text=back_to_menu_text, callback_data="back_to_params")]
    ])

    await query.message.edit_text(delete_text, reply_markup=kb)


@router.callback_query(lambda c: c.data == "yes")
async def confirm_delete_yes(query: CallbackQuery):
    user = await get_user_by_id(query.from_user.id)

    try:
        user_setting = TelegramUserSettings.objects.get(telegram_user=user)
        user_setting.delete()
        await query.message.edit_text(
            "Данные успешно удалены. Чтобы начать заново кликай --> /start" if user.lang == "rus" else
            "Деректер сәтті өшірілді. Қайта бастау үшін басыңыз --> /start"
        )
    except TelegramUserSettings.DoesNotExist:
        await query.message.edit_text(
            "Данных для удаления не найдено." if user.lang == "rus" else
            "Өшірілетін деректер табылмады."
        )


@router.callback_query(lambda c: c.data == "no")
async def confirm_delete_no(query: CallbackQuery):
    user = await get_user_by_id(query.from_user.id)
    await query.message.edit_text("Отменено." if user.lang == "rus" else "Бас тартылды.")
