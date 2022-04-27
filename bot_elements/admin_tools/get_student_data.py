from bots import admin_bot
from aiogram import types, Dispatcher
from bot_elements.admin_tools.displays import display_all_groups
from transliterate import translit

async def get_student_list_pdf(message: types.Message):
    group = message.text[18:].replace('_', '-') # получает ггуппу
    print(translit(group, 'ru'))
    # здесь пропиши путь к сгенерированному файлу


def register_handlers_get_data(dp: Dispatcher):
    dp.register_message_handler(
        display_all_groups, commands='get_student_list')
    dp.register_message_handler(
        get_student_list_pdf, lambda message: message.text.startswith('/get_student_list_'))
