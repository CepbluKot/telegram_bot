from aiogram import types
from operator import itemgetter
from bot_elements.storages.all_storages import temp_form_recipient_data 
from bot_elements.storages.all_storages import temp_mem_for_form_creator
from bot_elements.storages.all_storages import mem_for_created_forms
from bot_elements.storages.all_storages import send_forms_mem 
from bot_elements.storages.all_storages import completing_forms_dispatcher 
from bot_elements.storages.all_storages import registerData 
from bot_elements.storages.all_storages import temp_mem_for_answers
from bot_elements.storages.all_storages import edited_register_data
from bot_elements.storages.all_storages import choosing_groups_dispatcher
from bot_elements.storages.all_storages import temp_chosen_groups_data
from bot_elements.storages.all_storages import temp_form_index_data
import bot_elements.storages.all_storages
from bots import admin_bot, adminIds, student_bot, prepod_bot

from bot_elements.getter.all_getters import unconfirmed_users_get, registerData_get_role, registerData_check_is_in_register_list, registerData_get_group, registerData_get_fio, registerData_get_role, registerData_check_is_editing, edited_register_data_get_user, unconfirmed_users_get, unconfirmed_edit_users_get, registerData_check_is_confirmed
from bot_elements.remover.all_removers import edited_register_data_remove_user, registerData_remove_user
from fake_db.getters.all_getters import db_mem_for_created_forms_get_data
from fake_db.setters.all_setters import db_confirm_user, db_mem_for_created_forms_add_element, db_mem_for_created_forms_edit_poll_options, db_mem_for_created_forms_insert_question, db_mem_for_created_forms_set_new_form_name, db_mem_for_created_forms_set_new_question_name, db_registerData_add_user, db_registerData_change_data, db_send_forms_mem_add_completed_user, db_send_forms_mem_add_sent_form

def unconfirmed_users_plus_one():
    """ Увеличивает счетчик неподтвержденных пользователей на 1"""
    bot_elements.storages.all_storages.unconfirmed_register_users += 1


def unconfirmed_users_minus_one():
    """ Уменьшает счетчик неподтвержденных пользователей на 1"""
    bot_elements.storages.all_storages.unconfirmed_register_users -= 1


def unconfirmed_edit_users_plus_one():
    """ Увеличивает счетчик редактируемых пользователей на 1"""
    bot_elements.storages.all_storages.unconfirmed_edit_users += 1


def unconfirmed_edit_users_minus_one():
    """ Уменьшает счетчик редактируемых пользователей на 1"""
    bot_elements.storages.all_storages.unconfirmed_edit_users -= 1


def confirm_user(user_id: int):
    """ (Для БД) Подтверждает регистрацию пользователя"""
    """
        Пример registerData:
    {user_id: {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': True/False}, ...}
    """
    # registerData[user_id]['confirmed'] = True
    db_confirm_user(user_id)


def edited_register_data_set_new_data(new_chosen_fio: str, new_chosen_group: str, new_chosen_role: str, user_id: int):
    """ Вставляет запись с обновленными данными регистрации в edited_register_data"""
    """ Формат:
    {user_id: {'new_chosen_fio': chosen_fio, 'new_chosen_group': chosen_group, 'new_chosen_role': chosen_role, 'confirmed': False}}
    """
    edited_register_data[user_id] = {'new_chosen_fio': new_chosen_fio, 'new_chosen_group': new_chosen_group, 'new_chosen_role': new_chosen_role}


def edited_register_data_set_new_fio(new_chosen_fio: str, user_id: int):
    """ Изменяет ФИО в edited_register_data"""
    """ Формат:
    {user_id: {'new_chosen_fio': chosen_fio, 'new_chosen_group': chosen_group, 'new_chosen_role': chosen_role, 'confirmed': False}}
    """
    edited_register_data[user_id]['new_chosen_fio'] = new_chosen_fio


def edited_register_data_set_new_group(new_chosen_group: str, user_id: int):
    """ Изменяет группу в edited_register_data"""
    """ Формат:
    {user_id: {'new_chosen_fio': chosen_fio, 'new_chosen_group': chosen_group, 'new_chosen_role': chosen_role, 'confirmed': False}}
    """
    edited_register_data[user_id]['new_chosen_group'] = new_chosen_group


def temp_form_recipient_data_add_user_data(chat_id: int, form_name: str, type: str, form_id: int, creator_id: int):
    """ Добавляет даныне пользователя во временный словарь со служебными данными формы"""
    if not chat_id in temp_form_recipient_data:
        temp_form_recipient_data[chat_id] = {}

    temp_form_recipient_data[chat_id]["form_name"] = form_name
    temp_form_recipient_data[chat_id]["type"] = type
    temp_form_recipient_data[chat_id]["form_id"] = form_id
    temp_form_recipient_data[chat_id]["creator_id"] = creator_id


def temp_mem_for_form_creator_add_element(user_id: int, data: dict):
    """ Добавляет 1 элемент формы во временный словарь для создания формы"""
    """
        Формат поля data:
        (для просто вопроса) data={'question':'question', 'message_id': 0, 'type': 'msg'}
        (для опроса)         data={'question': 'question', 'options': ['options'], 'message_id': 0, 'type': 'poll'}
        (для служебной инфы) data={'form_name': 'Формо', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}
    """

    if user_id in temp_mem_for_form_creator:
            temp_mem_for_form_creator[user_id].append(data)
    else:
        temp_mem_for_form_creator[user_id] = [data]


def mem_for_created_forms_add_element(form_id: int, data):
    """ (Для БД) Добавляет 1 форму в словарь сохраненных форм"""
    """
        data - данные формы, form_id - айдишник формы
    """
    """ 
        Пример data:
    [{'question': 'opros', 'options': ['helicopter ', ' paracopter'], 'message_id': 0, 'type': 'poll'}, {'question': 'klava', 'message_id': 0, 'type': 'msg'}, {'form_name': 'formo', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}]
        
        Пример mem_for_created_forms:
        {*form_id*: [form data], ...}
    """
    # print(data)
    # mem_for_created_forms[form_id] = data
    db_mem_for_created_forms_add_element(form_id, data)


def mem_for_created_forms_insert_question(form_id: int, inser_after_id: int, data):
    """ (Для БД) Вставляет вопрос после выбранного id"""
    """
        form_id - айди формы, inser_after_id - айдишник вопроса после которого вставить текущий, data[0] - сами данные о вопросе
    """
    """
    Если надо, могу организовать через создание копии форм и добавляения вопроса в нее, псоле чего старые данные можно перезаписать этими
    """
    # mem_for_created_forms[form_id].insert(inser_after_id + 1, data[0])
    db_mem_for_created_forms_insert_question(form_id, inser_after_id, data)


async def mem_for_created_forms_set_new_form_name(form_id: int, new_form_name: str):
    """ (Для БД) Изменяет название формы из mem_for_created_forms"""

    """
        form_id - айди формы, new_form_name - новое название формы
    """
    """ 
        Пример mem_for_created_forms[form_id][-1]:
    {'form_name': 'formo', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}
    """
    # mem_for_created_forms[form_id][-1]['form_name'] = new_form_name
    db_mem_for_created_forms_set_new_form_name(form_id, new_form_name)


def mem_for_created_forms_set_new_question_name(form_id: int, question_id: int, new_question_name: str):
    """ (Для БД) Изменяет название вопроса формы из mem_for_created_forms"""
    """
        form_id - айди формы, question_id - айди вопроса, new_question_name - новое название вопроса
    """
    """ 
        Пример mem_for_created_forms[form_id][question_id]:
    {'question': 'opros', 'options': ['helicopter ', ' paracopter'], 'message_id': 0, 'type': 'poll'}
    """
    
    # mem_for_created_forms[form_id][question_id]['question'] = new_question_name
    db_mem_for_created_forms_set_new_question_name(form_id, question_id, new_question_name)

  
def mem_for_created_forms_edit_poll_options(form_id: int, question_id: int, new_poll_options: list):
    """ (Для БД) Изменяет опции опроса формы из mem_for_created_forms"""
    """
        form_id - айди формы, question_id - айди вопроса, new_poll_options - новые опции опроса
    """
    """ 
        Пример mem_for_created_forms[form_id][question_id]:
    {'question': 'opros', 'options': ['helicopter ', ' paracopter'], 'message_id': 0, 'type': 'poll'}
    """
    
    # mem_for_created_forms[form_id][question_id]['options'] = new_poll_options
    db_mem_for_created_forms_edit_poll_options(form_id, question_id, new_poll_options)
  


def send_forms_mem_add_sent_form(sent_form_id: int, form_id: int, form_creator_user_id: int, send_to_users_ids: list, groups: list):
    """ (Для БД) Добавляет 1 форму в список с отправленными формами"""
    """
        sent_form_id - айдишник отправленной формы, form_id - айдишник формы, form_creator_user_id - айдишник телеги создателя формы, send_to_users_ids - айдишники тех, кому придет опрос
    """
    """
        Пример send_forms_mem:
    {'sent_form_id': {'form_id': *form_id*, 'info': {'form_creator_user_id': id,'send_to_users_ids': [айдишники], 'send_to_groups': [groups],'got_answers_from': [айдишники]}, ...}
    """
    # send_forms_mem[sent_form_id] = {'form_id': form_id, 'info': {'form_creator_user_id': form_creator_user_id, 'send_to_users_ids': send_to_users_ids, 'send_to_groups': groups, 'got_answers_from': []}}
    db_send_forms_mem_add_sent_form(sent_form_id, form_id, form_creator_user_id, send_to_users_ids, groups)


async def send_forms_mem_add_completed_user(sent_form_id: int, user_id: int):
    """ (Для БД) Добавляет пользователя в список пользователей прошедших форму"""
    """
        sent_form_id - айдишник отправленной формы, , user_id - айди телеги пользователя, который прошел опрос
    """
    """
        Пример send_forms_mem[sent_form_id]['info']:
    {'form_creator_user_id': id,'send_to_users_ids': [айдишники], 'send_to_groups': [groups],'got_answers_from': [айдишники]}
    """
    # send_forms_mem[sent_form_id]['info']['got_answers_from'].append(user_id)
    await db_send_forms_mem_add_completed_user(sent_form_id, user_id)


def completing_forms_dispatcher_add_session(chat_id: int, unique_form_id: int, unique_sent_form_id: int):
    """ Добавляет 1 сессию в список активных сессий"""
    
    completing_forms_dispatcher[chat_id] = {
        'chat_id': chat_id, 'unique_form_id': unique_form_id, 'unique_sent_form_id': unique_sent_form_id, 'current_question_num': 0,'form_copy': db_mem_for_created_forms_get_data(unique_form_id)}
    

def completing_forms_dispatcher_add_1_to_question_num(user_id: int):
    """ Увеличивает на 1 номер текущего задаваемого вопроса"""
    completing_forms_dispatcher[user_id]['current_question_num'] += 1


def completing_forms_dispatcher_set_question_id(user_id: int, question_num: int, question_id: int):
    """ Задает id для сообщения формы"""
    completing_forms_dispatcher[user_id]['form_copy'][question_num]['message_id'] = question_id
    # print(completing_forms_dispatcher[user_id]['form_copy'][question_num])    


async def registerData_change_data(user_id: int, chosen_fio: str, chosen_group: str, chosen_role: str):
    
    """ (Для БД) Изменяет рег. данные пользователя"""
    """
        user_id -айди пользователя, chosen_fio - фио пользователя, chosen_group - группа, chosen_role - роль
    """
    """
        Пример registerData:
    {user_id: {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': True/False}, ...}
    """
    # registerData[user_id] = {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': True}
    db_registerData_change_data(user_id, chosen_fio, chosen_group, chosen_role)


async def registerData_add_user(user_id: int, chosen_fio: str, chosen_group: str, chosen_role: str):
    
    """ (Для БД) Добавляет рег. данные пользователя"""
    """
        user_id -айди пользователя, chosen_fio - фио пользователя, chosen_group - группа, chosen_role - роль
    """
    """
        Пример registerData:
    {user_id: {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': True/False}, ...}
    """

    unconfirmed_users_plus_one()

    for reciever in adminIds:
        await admin_bot.send_message(text='у вас ' + str(unconfirmed_users_get()) + ' неподтвержденных пользователей', chat_id=reciever)

    # registerData[user_id] = {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': False}
    db_registerData_add_user(user_id, chosen_fio, chosen_group, chosen_role)


async def registerData_change_group_data(user_id: int, new_group: str):
    """ Изменяет группу пользователя"""
    """
        user_id - айди пользователя, new_group - новая группа
    """

    if not registerData_check_is_editing(user_id):

        unconfirmed_edit_users_plus_one()
        edited_register_data_set_new_data(new_chosen_fio=registerData_get_fio(user_id), new_chosen_group=new_group, new_chosen_role=registerData_get_role(user_id), user_id=user_id)
    else:
        edited_register_data_set_new_group(new_chosen_group=new_group, user_id=user_id)

    for recipient in adminIds:
        await admin_bot.send_message(text=str(unconfirmed_edit_users_get()) + ' пользователей меняют свои данные', chat_id=recipient)


async def registerData_change_fio_data(user_id: int, new_fio: str):
    """ Изменяет ФИО пользователя"""
    """
        user_id -айди пользователя, new_fio - новые ФИО
    """
    if not registerData_check_is_editing(user_id):
        
        unconfirmed_edit_users_plus_one()
        edited_register_data_set_new_data(new_chosen_fio=new_fio, new_chosen_group=registerData_get_group(user_id), new_chosen_role=registerData_get_role(user_id), user_id=user_id)
    
    else:
        edited_register_data_set_new_fio(new_chosen_fio=new_fio, user_id=user_id)

    for recipient in adminIds:
        await admin_bot.send_message(text=str(unconfirmed_edit_users_get()) + ' пользователей меняют свои данные', chat_id=recipient)
    

async def registerData_accept_register(user_id: int, message: types.Message):
    """ Подтверждает регистрацию пользователя"""
    """
        user_id -айди пользователя
    """
    if registerData_check_is_in_register_list(user_id) and not registerData_check_is_confirmed(user_id):
        await message.answer('Пользователь ' + str(user_id) + ' подтвержден')

        if registerData_get_role(user_id=user_id) == 'prepod':
            await prepod_bot.send_message(chat_id=user_id, text='Ваша регистрация подтверждена админом')
        
        elif registerData_get_role(user_id=user_id) == 'student':
            await student_bot.send_message(chat_id=user_id, text='Ваша регистрация подтверждена админом')
        
        confirm_user(user_id)
        
        unconfirmed_users_minus_one()

    else:
        await message.answer('Пользователя нет в списке на подтверждение регистрации')


async def registerData_deny_register(user_id: int, message: types.Message):
    """ Не подтверждает регистрацию пользователя"""
    """
        user_id -айди пользователя
    """
    if registerData_check_is_in_register_list(user_id) and not registerData_check_is_confirmed(user_id):
        await message.answer('Пользователь ' + str(user_id) + ' отправлен на повторную регистрацию')

        if registerData_get_role(user_id=user_id) == 'prepod':
            await prepod_bot.send_message(chat_id=user_id, text='Ваша регистрация не подтверждена админом, пожалуйста, зарегистрируйтесь заново с корректными данными')
        
        elif registerData_get_role(user_id=user_id) == 'student':
            await student_bot.send_message(chat_id=user_id, text='Ваша регистрация не подтверждена админом, пожалуйста, зарегистрируйтесь заново с корректными данными')
        
        registerData_remove_user(user_id)
        unconfirmed_users_minus_one()

    else:
        await message.answer('Пользователя нет в списке на подтверждение регистрации')


async def registerData_accept_register_edit(user_id: int, message: types.Message):
    """ Подтверждает регистрацию пользователя"""
    """
        user_id -айди пользователя
    """
    if registerData_check_is_editing(user_id):

        await message.answer('Изменение данных пользователя ' + str(user_id) + ' подтверждено')
        new_data = edited_register_data_get_user(user_id)

        if registerData_get_role(user_id=user_id) == 'prepod':
            await prepod_bot.send_message(chat_id=user_id, text='Изменение ваших рег. данных подтверждено админом\n' + 'Ваши новые данные: ФИО: ' + str(new_data['new_chosen_fio']))
        
        elif registerData_get_role(user_id=user_id) == 'student':
            await student_bot.send_message(chat_id=user_id, text='Изменение ваших рег. данных подтверждено админом\n' + 'Ваши новые данные: ФИО: ' + str(new_data['new_chosen_fio']) + ' ГРУППА: ' + str(new_data['new_chosen_group']))
        
        await registerData_change_data(user_id=user_id, chosen_fio=new_data['new_chosen_fio'], chosen_group=new_data['new_chosen_group'], chosen_role=new_data['new_chosen_role'])
        
        edited_register_data_remove_user(user_id)
        unconfirmed_edit_users_minus_one()

    else:
        await message.answer('Пользователя нет в списке на изменение регистрации')


async def registerData_deny_register_edit(user_id: int, message: types.Message):
    """ Не подтверждает регистрацию пользователя"""
    """
        user_id -айди пользователя
    """
    if registerData_check_is_editing(user_id): 
        await message.answer('Пользователю ' + str(user_id) + ' отказано в изменении рег. данных')

        if registerData_get_role(user_id=user_id) == 'prepod':
            await prepod_bot.send_message(chat_id=user_id, text='Изменение ваших рег. данных не подтверждено админом, при необходимости, заново введите корректные рег. данные')
        
        elif registerData_get_role(user_id=user_id) == 'student':
            await student_bot.send_message(chat_id=user_id, text='Изменение ваших рег. данных не подтверждено админом, при необходимости, заново введите корректные рег. данные')
        
        edited_register_data_remove_user(user_id)
        unconfirmed_edit_users_minus_one()
    else:
        await message.answer('Пользователя нет в списке на изменение регистрации')


def unique_form_id_plus_one():
    """ Увеличивает счетчик созданных вопросов на 1"""
    bot_elements.storages.all_storages.unique_form_id += 1


def unique_sent_form_id_plus_one():
    """ Увеличивает счетчик отправленных вопросов на 1"""
    bot_elements.storages.all_storages.unique_sent_form_id += 1


def sendPollAnswer(pollAnswer: types.PollAnswer, question_number: int, unique_form_id: int, unique_sent_form_id: int, pollCopy):
    """ Получает ответ на опрос"""
    if not pollAnswer.user.id in temp_mem_for_answers.keys():
        temp_mem_for_answers[pollAnswer.user.id] = []
    
    temp_mem_for_answers[pollAnswer.user.id].append({'pollAnswer': pollAnswer, 'question_number': question_number, 'unique_form_id': unique_form_id, 'unique_sent_form_id': unique_sent_form_id, 'pollCopy': pollCopy})
    

def sendMsgAnswer(messageAnswer: types.Message, question_number: int, unique_form_id: int, unique_sent_form_id: int, messageCopy):
    """ Получает ответ на текстовый вопрос"""
    # print('\n', messageAnswer, question_number, unique_form_id, unique_sent_form_id, messageCopy)
    if not messageAnswer.chat.id in temp_mem_for_answers.keys():
        temp_mem_for_answers[messageAnswer.chat.id] = []
    
    temp_mem_for_answers[messageAnswer.chat.id].append({'messageAnswer': messageAnswer, 'question_number': question_number, 'unique_form_id': unique_form_id, 'unique_sent_form_id': unique_sent_form_id, 'messageCopy': messageCopy})


def sendFormAnswer(formAnswer: dict):
    """ Сюда приходит словарь со всеми ответами на форму"""
    print(formAnswer)
    pass

# ---- дальше забей ----

def choosing_groups_dispatcher_add_user(user_id: int, poll_id: int, options: list, poll_number: int):
    """
    Формат:
        {user_id: [poll_number: {'poll_id': , 'poll_options': }, 1: ...], ...}   
    """

    if not user_id in choosing_groups_dispatcher.keys():
        choosing_groups_dispatcher[user_id] = {}

    choosing_groups_dispatcher[user_id][poll_number] = {'poll_id': poll_id, 'options': options}


def chosen_groups_data_add_group(user_id: int, options_ids: list, groups: list):
    if not user_id in temp_chosen_groups_data.keys():
        temp_chosen_groups_data[user_id] = []
    
    # print('\n\n',groups, options_ids)

    

    selected_groups = itemgetter(*options_ids)(groups)
   
    temp_chosen_groups_data[user_id].extend([selected_groups])
    print('\n\nfak', temp_chosen_groups_data)


def temp_form_index_data_add_index(user_id: int, form_index: int):
    temp_form_index_data[user_id] = form_index
