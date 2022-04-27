from bot_elements.getter.all_getters import registerData_get, edited_register_data_get
from bot_elements.setter.all_setters import registerData_accept_register, registerData_deny_register, registerData_accept_register_edit, registerData_deny_register_edit
from aiogram import types, Dispatcher


async def display_unregistered_users(message: types.Message):
    """ Формат
      user_id :  {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': False}
    """
    registerData = registerData_get()
    if registerData:
        full_text = ''
        count = 1
        for user_id in registerData:
            
            selected_user_data = registerData[user_id]
            if selected_user_data['chosen_role'] == 'student' and not selected_user_data['confirmed']:
                full_text += str(count) + ') ФИО: ' + str(selected_user_data['chosen_fio']) + ' ГРУППА: ' + str(selected_user_data['chosen_group']) + ' РОЛЬ: ' + str(selected_user_data['chosen_role']) + ' /acceptReg_' + str(user_id) + ' /denyReg_' + str(user_id) +'\n'
            
            elif selected_user_data['chosen_role'] == 'prepod' and not selected_user_data['confirmed']:
                full_text += str(count) + ') ФИО: ' + str(selected_user_data['chosen_fio']) + ' РОЛЬ: ' + str(selected_user_data['chosen_role']) + ' /acceptReg_' + str(user_id) + ' /denyReg_' + str(user_id) +'\n'
            
            count += 1

        if not full_text:
            await message.answer(' Нет неподтвержденных пользователей')
        
        else:
            await message.answer(full_text)
    else:
        await message.answer(' Нет неподтвержденных пользователей')


async def display_edited_users(message: types.Message):
    
    registerData = edited_register_data_get()
    if registerData:
        full_text = ''
        count = 1
        for user_id in registerData:
            
            selected_user_data = registerData[user_id]
            if selected_user_data['new_chosen_role'] == 'student':
                full_text += str(count) + ') ФИО: ' + str(selected_user_data['new_chosen_fio']) + ' ГРУППА: ' + str(selected_user_data['new_chosen_group']) + ' РОЛЬ: ' + str(selected_user_data['new_chosen_role']) + ' /acceptEdit_' + str(user_id) + ' /denyEdit_' + str(user_id) +'\n'
            
            elif selected_user_data['new_chosen_role'] == 'prepod':
                full_text += str(count) + ') ФИО: ' + str(selected_user_data['new_chosen_fio']) + ' РОЛЬ: ' + str(selected_user_data['new_chosen_role']) + ' /acceptEdit_' + str(user_id) + ' /denyEdit_' + str(user_id) +'\n'
            
            count += 1
        await message.answer(full_text)
    else:
        await message.answer(' Никто не изменяет рег. данные')


async def accept_register(message: types.Message):
    user_id = int(message.text[11:])
    await registerData_accept_register(user_id=user_id, message=message)
    

async def deny_register(message: types.Message):
    user_id = int(message.text[9:])
    await registerData_deny_register(user_id=user_id, message=message)
    

async def accept_register_edit(message: types.Message):
    user_id = int(message.text[12:])
    await registerData_accept_register_edit(user_id=user_id, message=message)
    

async def deny_register_edit(message: types.Message):
    user_id = int(message.text[10:])
    await registerData_deny_register_edit(user_id=user_id, message=message)


def register_handlers_forms_check_register(dp: Dispatcher):
    dp.register_message_handler(
        display_unregistered_users, commands='check_unregistered_users')
    
    dp.register_message_handler(
        display_edited_users, commands='check_edited_users')

    dp.register_message_handler(accept_register, lambda message: message.text.startswith('/acceptReg_'))
    dp.register_message_handler(deny_register, lambda message: message.text.startswith('/denyReg_'))

    dp.register_message_handler(accept_register_edit, lambda message: message.text.startswith('/acceptEdit_'))
    dp.register_message_handler(deny_register_edit, lambda message: message.text.startswith('/denyEdit_'))
