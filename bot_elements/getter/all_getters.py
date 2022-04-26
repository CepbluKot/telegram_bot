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
from fake_db.getters.all_getters import db_get_group_users_ids, db_mem_for_created_forms_get, db_mem_for_created_forms_get_creator_id, db_mem_for_created_forms_get_data, db_mem_for_created_forms_get_form_name, db_registerData_check_is_confirmed, db_registerData_check_is_in_register_list, db_registerData_check_is_registered, db_registerData_get, db_registerData_get_fio, db_registerData_get_group, db_registerData_get_role, db_send_forms_mem_get, db_send_forms_mem_get_form, db_send_forms_mem_get_form_completed_users, db_send_forms_mem_get_form_sent_users, db_unique_form_id_get, db_unique_sent_form_id_get


def temp_form_recipient_data_get_data(user_id: int):
    """ Возвращает временную ячейку памяти хранящую служебные данные (temp_form_recipient_data)"""
    return temp_form_recipient_data[user_id]


def temp_mem_for_form_creator_get_data(user_id: int):
    """ Возвращает временную ячейку памяти хранящую данные создаваемой формы (temp_mem_for_form_creator)"""
    return temp_mem_for_form_creator[user_id]


def temp_mem_for_form_creator_get():
    """ Возвращает словарь с инфой о формах которые юзеры создают в наст. момент (temp_mem_for_form_creator)"""
    return temp_mem_for_form_creator


def temp_form_recipient_data_get_form_id(user_id: int):
    """  Возвращает айди формы из временного словаря со служебной инфой"""
    return temp_form_recipient_data[user_id]['form_id']


def temp_form_recipient_data_get_recip_data(user_id: int):
    """  Возвращает временный словарь со служебной инфой"""
    return temp_form_recipient_data[user_id]


def temp_form_recipient_data_get():
    """  Возвращает temp_form_recipient_data (словарь создаваемых в наст. момент форм)"""
    return temp_form_recipient_data


def mem_for_created_forms_get():
    """ (Для БД) Возвращает mem_for_created_forms"""
    """
        Пример mem_for_created_forms:
    {0: [{'question': 'Сос', 'options': ['Лан', ' все'], 'message_id': 0, 'type': 'poll'}, {'question': 'Месяц', 'message_id': 0, 'type': 'msg'}, {'form_name': 'Формо', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}], 1: [{'question': 'Зе криэтир', 'options': ['Один', ' два'], 'message_id': 0, 'type': 'poll'}, {'form_name': 'Тайлер', 'type': 'info', 'form_id': 1, 'creator_id': 506629389}]}
    """
    # return mem_for_created_forms
    return db_mem_for_created_forms_get()


def mem_for_created_forms_get_data(form_id: int):
    """ (Для БД) Возвращает ячейку памяти хранящую данные созданной формы (mem_for_created_forms)"""
    """
        form_id - айди формы
        Пример mem_for_created_forms[form_id]:
    [{'question': 'Сос', 'options': ['Лан', ' все'], 'message_id': 0, 'type': 'poll'}, {'question': 'Месяц', 'message_id': 0, 'type': 'msg'}, {'form_name': 'Формо', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}]
    """
    # return mem_for_created_forms[form_id]
    return db_mem_for_created_forms_get_data(form_id)


def mem_for_created_forms_get_form_name(form_id: int):
    """ (Для БД) Возвращает название созданной формы из mem_for_created_forms"""
    """
        form_id - айди формы
        Пример mem_for_created_forms[form_id][-1]:
    {'form_name': 'Формо', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}
    """
    # return mem_for_created_forms[form_id][-1]['form_name']
    return db_mem_for_created_forms_get_form_name(form_id)


def mem_for_created_forms_get_creator_id(form_id: int):
    """ (Для БД) Возвращает айди создателя формы из mem_for_created_forms"""
    """
        form_id - айди формы
        Пример mem_for_created_forms[form_id][-1]:
    {'form_name': 'Формо', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}
    """
    # return mem_for_created_forms[form_id][-1]['creator_id']
    return db_mem_for_created_forms_get_creator_id(form_id)


def completing_forms_dispatcher_get_form_copy(user_id: int):
    """ Возвращает копию формы из completing_forms_dispatcher"""
    return completing_forms_dispatcher[user_id]['form_copy']


def completing_forms_dispatcher_get_form_question_copy(user_id: int, question_num: int):
    """ Возвращает копию вопроса из формы"""
    return completing_forms_dispatcher[user_id]['form_copy'][question_num]


def completing_forms_dispatcher_get_form_question_message_id(user_id: int, question_num: int):
    """ Возвращает айди сообщения(опроса) по номеру вопроса из completing_forms_dispatcher"""
    return completing_forms_dispatcher[user_id]['form_copy'][question_num]['message_id']


def completing_forms_dispatcher_get_current_question_num(user_id: int):
    """ Возвращает номер текущего вопроса из completing_forms_dispatcher"""
    return completing_forms_dispatcher[user_id]['current_question_num']


def completing_forms_dispatcher_get_question_by_num(user_id: int, question_num: int):
    """ Возвращает вопрос по номеру вопроса из completing_forms_dispatcher"""
    return completing_forms_dispatcher[user_id]['form_copy'][question_num]


def completing_forms_dispatcher_get_form_id(user_id: int):
    """ Возвращает айди сохраненной формы по юзер айди из completing_forms_dispatcher"""
    return completing_forms_dispatcher[user_id]['unique_form_id']


def completing_forms_dispatcher_get_sent_form_id(user_id: int):
    """ Возвращает айди отправленной формы по юзер айди из completing_forms_dispatcher"""
    return completing_forms_dispatcher[user_id]['unique_sent_form_id']


def completing_froms_dispatcher_is_user_in_list(user_id: int):
    """ Проверяет, заполняет ли сейчас пользователь форму"""
    return user_id in completing_forms_dispatcher.keys()


def completing_forms_dispatcher_get():
    """ Возвращает completing_forms_dispatcher (список с юзерами и  формами которые они сейчас заполняют)"""
    return completing_forms_dispatcher


def registerData_get():
    """ (Для БД) возвращает registerData"""
    """ 
        Пример registerData:
    {user_id: {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': True/False}, ...}
    """
    # return registerData
    return db_registerData_get()


def registerData_get_fio(user_id: int):
    """ (Для БД) Возвращает ФИО юзера из registerData"""
    """ 
        Пример registerData[user_id]:
    {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': True/False}
    """
    # return registerData[user_id]['chosen_fio']
    return db_registerData_get_fio(user_id)


def registerData_get_group(user_id: int):
    """ (Для БД) Возвращает группу юзера из registerData"""
    """ 
        Пример registerData[user_id]:
    {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': True/False}
    """
    
    # return registerData[user_id]['chosen_group']
    return db_registerData_get_group(user_id)


def registerData_get_role(user_id: int):
    """ (Для БД) Возвращает роль юзера из registerData"""
    """ 
        Пример registerData[user_id]:
    {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': True/False}
    """

    # return registerData[user_id]['chosen_role']
    return db_registerData_get_role(user_id)


def registerData_check_is_in_register_list(user_id: int):
    """ (Для БД) Проверяет есть ли юзер в registerData"""

    """ user_id - айди юзера (эта функция по факту повторяется, но она нужна)"""
    # return user_id in registerData.keys()
    return db_registerData_check_is_in_register_list(user_id)


def registerData_check_is_registered(user_id: int):
    """ (Для БД) Проверяет есть ли юзер в registerData"""
    """ 
        Формат registerData:
        {user_id: {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': False}, ...}
    """
    # if user_id in registerData.keys():
    #     print(registerData[user_id]['confirmed'])
    #     return registerData[user_id]['confirmed']
    # else:
    #     return False
    return db_registerData_check_is_registered(user_id)


def registerData_check_is_confirmed(user_id: int):
    """ (Для БД) Проверяет подтвержден ли юзер в registerData"""

    """ user_id - айди юзера"""
    """ 
        Пример registerData[user_id]:
    {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': True/False}
    """
    return db_registerData_check_is_confirmed(user_id)


    # if user_id in registerData.keys():

    #     return registerData[user_id]['confirmed']


def registerData_check_is_editing(user_id: int):
    """ Проверяет находится ли пользователь в edited_register_data (словарь с обновленныит рег данными пользователей, которые пока не подтвердил админ)"""
    """
        Пример edited_register_data
    {user_id: {'new_chosen_fio': chosen_fio, 'new_chosen_group': chosen_group, 'new_chosen_role': chosen_role}, ...}
    """
    return user_id in edited_register_data.keys()


def edited_register_data_get():
    """ Возвращает edited_register_data"""
    """ Пример edited_register_data
    {user_id: {'new_chosen_fio': chosen_fio, 'new_chosen_group': chosen_group, 'new_chosen_role': chosen_role, 'confirmed': False}}
    """
    return edited_register_data


def edited_register_data_get_user(user_id: int):
    """ Возвращает данные пользователя из edited_register_data"""
    """ Пример edited_register_data[user_id]:
    {'new_chosen_fio': chosen_fio, 'new_chosen_group': chosen_group, 'new_chosen_role': chosen_role, 'confirmed': False}
    """
    return edited_register_data[user_id]


def edited_register_data_get_fio(user_id: int):
    """ Возвращает обновленное ФИО пользователя из edited_register_data"""
    """ Пример edited_register_data[user_id]:
    {user_id: {'new_chosen_fio': chosen_fio, 'new_chosen_group': chosen_group, 'new_chosen_role': chosen_role, 'confirmed': False}}
    """
    return edited_register_data[user_id]['new_chosen_fio']


def edited_register_data_get_group(user_id: int):
    """  Возвращает обновленную группу пользователя из edited_register_data"""
    """ Пример edited_register_data[user_id]:
    {user_id: {'new_chosen_fio': chosen_fio, 'new_chosen_group': chosen_group, 'new_chosen_role': chosen_role, 'confirmed': False}}
    """
    return edited_register_data[user_id]['new_chosen_group']


def send_forms_mem_get():
    """ (Для БД) Возвращает send_forms_mem (память с отправленынми формами)"""
    """ 
    Формат send_forms_mem
    {'sent_form_id': {'form_id': *form_id*, 'info': {'form_creator_user_id': id,'send_to_users_ids': [ids], 'got_answers_from': [ids]}, ...} 
    
    """
    # return send_forms_mem
    return db_send_forms_mem_get()


def send_forms_mem_get_form(sent_form_id: int):
    """ (Для БД) Возвращает форму из send_forms_mem (память с отправленынми формами)"""

    """ sent_form_id - айди отправленной формы"""

    """ 
    Формат send_forms_mem[sent_form_id]
    {'form_id': *form_id*, 'info': {'form_creator_user_id': id,'send_to_users_ids': [айдишники], 'got_answers_from': [айдишники]}}
    """
    # return send_forms_mem[sent_form_id]
    return db_send_forms_mem_get_form(sent_form_id)


def send_forms_mem_get_form_sent_users(sent_form_id: int):
    """ (Для БД) Возвращает айди пользователей, которым отослана форма"""

    """ sent_form_id - айди отправленной формы"""

    """ 
    Формат send_forms_mem[sent_form_id]['info']
    {'form_creator_user_id': id,'send_to_users_ids': [айдишники], 'got_answers_from': [айдишники]}
    """
    # return send_forms_mem[sent_form_id]['info']['send_to_users_ids']
    return db_send_forms_mem_get_form_sent_users(sent_form_id)


def send_forms_mem_get_form_completed_users(sent_form_id: int):
    """ (Для БД) Возвращает айди пользователей, которые прошли форму"""

    """ sent_form_id - айди отправленной формы"""

    """ 
    Формат send_forms_mem[sent_form_id]['info']
    {'form_creator_user_id': id,'send_to_users_ids': [айдишники], 'got_answers_from': [айдишники]}
    """
    # return send_forms_mem[sent_form_id]['info']['got_answers_from']
    return db_send_forms_mem_get_form_completed_users(sent_form_id)


def unique_form_id_get():
    """ (Для БД) Возвращает счетчик созданных форм"""
    # print(' \n\nloool unique_form_id ', bot_elements.storages.all_storages.unique_form_id)
    # return bot_elements.storages.all_storages.unique_form_id
    return db_unique_form_id_get()


def unique_sent_form_id_get():
    """ (Для БД) Возвращает счетчик отправленных форм"""
    # print('unique_sent_form_id ',bot_elements.storages.all_storages.unique_sent_form_id)
    # return bot_elements.storages.all_storages.unique_sent_form_id
    return db_unique_sent_form_id_get()


def unconfirmed_users_get():
    """ Возвращает счетчик регистраций, которые ожидают подтверждения админа"""
    # print('unique_sent_form_id ',bot_elements.storages.all_storages.unique_sent_form_id)
    return bot_elements.storages.all_storages.unconfirmed_register_users


def unconfirmed_edit_users_get():
    """ Возвращает счетчик регистраций с обновленными данными, которые ожидают подтверждения админа"""
    return bot_elements.storages.all_storages.unconfirmed_edit_users


def temp_mem_for_answers_get():
    """ Возвращает все ответы на вопросы формы"""
    return temp_mem_for_answers


def get_all_groups():
    """ (Для БД) Возвращает список всех групп"""
    all_groups = ['М3О-212Б-20', 'М3О-214Б-20', 'М3О-309Б-19', 'М3О-314Б-19', 'М3О-118М-21',
              'М3О-111М-21',  'М3О-214Б-20', 'М3О-221Б-20', 'М3О-309Б-19', 'М3О-314Б-19']

    return all_groups


def get_group_users_ids(groups: list):
    """ (Для БД) Возвращает список айдишников студентов из выбранных групп"""
    """ groups - список с группами"""

    return db_get_group_users_ids(groups)


def get_document(form_id: int, sent_form_id: int): # Илья сюда
    """ (Для БД) Возвращает pdf документ с результатом формы"""
    """ form_id - айдишник формы, sent_form_id - айдишник отправленной формы"""

    pass


# ---- дальше забей ------------
def get_choosing_groups_dispatcher_user(user_id: int):
    """
        Формат:
            {user_id: {poll_number: {'poll_id': , 'poll_options': }, 1: {...}, ...}   
    """
    if user_id in choosing_groups_dispatcher.keys():
        return choosing_groups_dispatcher[user_id]

    else:
        return False


def get_chosen_groups_data(user_id: int):
    if user_id in temp_chosen_groups_data.keys():
        return temp_chosen_groups_data[user_id]
    

def get_temp_form_index_data(user_id: int):
    return temp_form_index_data[user_id]
