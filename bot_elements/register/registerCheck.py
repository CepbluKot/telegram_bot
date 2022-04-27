from aiogram import types, Dispatcher
from bot_elements.getter.all_getters import registerData_check_is_registered


async def checker(message: types.Message):
    
    if not registerData_check_is_registered(message.chat.id):
        
        await message.answer(' Вы не можете ничего делать, пока вы не зарегистрированы')
    else:
        await message.answer(' Вы не можете ничего делать, пока ваша регистарция не подтверждена')


def register_handlers_register_check(dp: Dispatcher):
    dp.register_message_handler(
        checker, lambda message: (not registerData_check_is_registered(message.chat.id)) and message.text.startswith('/'))
