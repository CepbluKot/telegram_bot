import asyncio
import bot_elements.raspisanie.raspisanie as raspisanie
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from bot_elements.register.prepod_register import register_handlers_register_prepod
from bot_elements.register.student_register import register_handlers_register_student


from bot_elements.forms.forms import register_handlers_forms
from bot_elements.forms.forms_menu import register_handlers_forms_menu
from bot_elements.status.student_status import register_handlers_student_status
from bot_elements.status.prepod_status import register_handlers_prepod_status
from bot_elements.forms.forms_editor import register_handlers_forms_editor
from bot_elements.cancel import register_handlers_cancel
from bot_elements.admin_tools.check_storages import register_handlers_forms_check_storages
from bot_elements.admin_tools.aproove_register import register_handlers_forms_check_register

from bot_elements.register.registerCheck import register_handlers_register_check
from bot_elements.admin_tools.get_student_data import register_handlers_get_data

from bots import student_bot, prepod_bot, admin_bot

async def prepod_commands(bot: Bot):
    prepod_commands = [
        BotCommand(command="/register", description="Регистация"),
        BotCommand(command="/multi_form", description="Создать форму"),
        BotCommand(command="/saved_forms",
                   description="Посмотреть сохраненные формы"),
        BotCommand(command="/status", description="Отобразить статус"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]

    await bot.set_my_commands(prepod_commands)


async def student_commands(bot: Bot):
    student_commands = [
        BotCommand(command="/register", description="Регистация"),
        BotCommand(command="/status", description="Полученные формы"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(student_commands)


async def admin_commands(bot: Bot):
    student_commands = [
        BotCommand(command="/check_current_creating_forms", description="Создаваемые сейчас формы"),
        BotCommand(command="/check_created_forms", description="Все созданные формы"),
        BotCommand(command="/check_sent_forms", description="Отправленные формы"),
        BotCommand(command="/check_completing_forms", description="Выполняемые формы"),
        BotCommand(command="/check_unregistered_users", description="Пользователи, ожидающие подтверждения регистрации"),
        BotCommand(command="/check_edited_users", description="Пользователи, ожидающие подтверждения изменения данных"),
        BotCommand(command="/get_student_list", description="Получить список студентов по группе (напишите номер группы)"),
    ]
    await bot.set_my_commands(student_commands)


async def main():
    
    
    prepod_bot_dispatcher = Dispatcher(prepod_bot, storage=MemoryStorage(),
                    loop=asyncio.get_event_loop())
    
    student_bot_dispatcher = Dispatcher(student_bot, storage=MemoryStorage(),
                    loop=asyncio.get_event_loop())

    admin_bot_dispatcher = Dispatcher(admin_bot, storage=MemoryStorage(),
                    loop=asyncio.get_event_loop())

    prepod_bot_dispatcher.loop.create_task(prepod_commands(prepod_bot))
    student_bot_dispatcher.loop.create_task(student_commands(student_bot))
    admin_bot_dispatcher.loop.create_task(admin_commands(admin_bot))
    # dp.loop.create_task(raspisanie.rasp_notification('М3О-221Б-20'))
    

    register_handlers_cancel(prepod_bot_dispatcher)
    register_handlers_cancel(student_bot_dispatcher)


    register_handlers_register_prepod(prepod_bot_dispatcher)
    register_handlers_register_student(student_bot_dispatcher)

    
    register_handlers_register_check(prepod_bot_dispatcher)
    register_handlers_register_check(student_bot_dispatcher)


    register_handlers_forms_editor(prepod_bot_dispatcher)
    register_handlers_forms(prepod_bot_dispatcher)
    register_handlers_forms_menu(prepod_bot_dispatcher)
    register_handlers_prepod_status(prepod_bot_dispatcher)
    
#     dp.register_message_handler(not_confirmed, lambda message: registerData_confirmed_check(message.chat.id), commands="status")

    
    # register_handlers_forms_editor(student_bot_dispatcher)
    # register_handlers_forms(student_bot_dispatcher)
    # register_handlers_forms_menu(student_bot_dispatcher)
    register_handlers_student_status(student_bot_dispatcher)

    # register_handlers_register_admin(admin_bot_dispatcher)
    register_handlers_forms_check_storages(admin_bot_dispatcher)
    register_handlers_forms_check_register(admin_bot_dispatcher)
    register_handlers_get_data(admin_bot_dispatcher)
    await asyncio.gather(prepod_bot_dispatcher.start_polling(), student_bot_dispatcher.start_polling(), admin_bot_dispatcher.start_polling())
    

asyncio.run(main())
