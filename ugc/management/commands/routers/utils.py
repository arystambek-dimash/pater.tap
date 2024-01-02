from django.core.exceptions import ObjectDoesNotExist

from ugc.models import TelegramUser


async def edit_message_text(message, text, kb=None):
    if not kb:
        await message.edit_text(text)
    else:
        await message.edit_text(text, reply_markup=kb)


async def change_language(language, callback_query=None):
    user_id = callback_query.from_user.id if callback_query else None
    username = callback_query.from_user.username if callback_query else None

    user, created = await get_or_create_user(user_id, username, language)
    first_name = callback_query.from_user.first_name
    user.set_language(language)
    confirmation_message = {
        "rus": f"Язык изменен на 🇷🇺 русский язык для пользователя {first_name}.",
        "kaz": f"Тіл 🇰🇿 қазақ тіліне өзгерді, пайдаланушы {first_name} үшін.",
    }[language] if not created else {
        "rus": f"Русский язык установлен для пользователя {first_name}.",
        "kaz": f"Қазақ тілі пайдаланушы {first_name} үшін орнатылды.",
    }[language]
    await edit_message_text(callback_query.message, confirmation_message)


async def get_or_create_user(user_id, username, language):
    return TelegramUser.objects.get_or_create(
        user_id=user_id,
        defaults={"username": username, "lang": language},
    )


async def get_user_by_id(user_id):
    try:
        return TelegramUser.objects.get(user_id=user_id)
    except ObjectDoesNotExist:
        return None
