from bot_elements.storages.all_storages import temp_form_recipient_data 
from bot_elements.storages.all_storages import temp_mem_for_form_creator
from bot_elements.storages.all_storages import mem_for_created_forms
from bot_elements.storages.all_storages import send_forms_mem 
# temp_mem_for_form_creator + temp_poll_recip_data -> mem_for_created_forms -> send_forms_mem -> completing_forms_dispatcher

from bot_elements.storages.all_storages import completing_forms_dispatcher # {'user_id': {''unique_form_id'': id, 'unique_sent_form_id': id, 'curr_page': num, 'form_copy': [form_data]}, ...}
from bot_elements.storages.all_storages import registerData # {*user_id*: {'user_role': *role*, 'user_group': *group*}}


def temp_form_recipient_data_add_user_data(chat_id: int, form_name: str, type: str, form_id: int, creator_id: int):
    """Добавляет даныне пользователя во временный словарь со служебными данными формы"""
    if not chat_id in temp_form_recipient_data:
        temp_form_recipient_data[chat_id] = {}

    temp_form_recipient_data[chat_id]["form_name"] = form_name
    temp_form_recipient_data[chat_id]["type"] = type
    temp_form_recipient_data[chat_id]["form_id"] = form_id
    temp_form_recipient_data[chat_id]["creator_id"] = creator_id


def temp_mem_for_form_creator_add_element(user_id: int, data: dict):
    """Добавляет 1 элемент формы во временный словарь для создания формы"""
    if user_id in temp_mem_for_form_creator:
            temp_mem_for_form_creator[user_id].append(data)
    else:
        temp_mem_for_form_creator[user_id] = [data]


def mem_for_created_forms_add_element(user_id: int, data):
    """Добавляет 1 форму в словарь сохраненных форм"""
    mem_for_created_forms[user_id] = data


def send_forms_mem_add_sent_form(form_id: int, sent_form_id: int, form_creator_user_id: int, send_to_users_ids: list):
    """Добавляет 1 форму в список с отправленными формами"""
    send_forms_mem.append({'form_id': form_id, 'sent_form_id': sent_form_id, 'info': {'form_creator_user_id': form_creator_user_id, 'send_to_users_ids': send_to_users_ids}})
    

def completing_forms_dispatcher_add_session(chat_id: int, unique_form_id: int, unique_sent_form_id: int):
    """Добавляет 1 сессию в список активных сессий"""
    completing_forms_dispatcher[chat_id] = {
        'chat_id': chat_id, 'unique_form_id': unique_form_id, 'unique_sent_form_id': unique_sent_form_id, 'form_copy': mem_for_created_forms[unique_form_id]}
    

def registerData_add_user(user_id: int, chosen_fio: str, chosen_group: str, chosen_role: str):
    """Добавляет рег. данные пользователя"""
    registerData[user_id] = {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role}


def registerData_change_group_data(user_id: int, new_group: str):
    """Изменяет группу пользователя"""
    registerData[user_id]['chosen_group'] = new_group
    

def registerData_change_fio_data(user_id: int, new_fio: str):
    """Изменяет ФИО пользователя"""
    registerData[user_id]['chosen_fio'] = new_fio