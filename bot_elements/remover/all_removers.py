from bot_elements.storages.all_storages import temp_form_recipient_data 
from bot_elements.storages.all_storages import temp_mem_for_form_creator
from bot_elements.storages.all_storages import mem_for_created_forms
from bot_elements.storages.all_storages import send_forms_mem
from bot_elements.storages.all_storages import completing_forms_dispatcher 
from bot_elements.storages.all_storages import registerData
from bot_elements.storages.all_storages import edited_register_data
from bot_elements.storages.all_storages import choosing_groups_dispatcher
from bot_elements.storages.all_storages import temp_chosen_groups_data
from bot_elements.storages.all_storages import temp_form_index_data
from fake_db.removers.all_removers import db_mem_for_created_forms_delete_form, db_mem_for_created_forms_delete_question, db_registerData_remove_user
# temp_mem_for_form_creator + temp_poll_recip_data -> mem_for_created_forms -> send_forms_mem -> completing_forms_dispatcher


def temp_form_recipient_data_remove_element(user_id: int):
    """ Убирает 1 элемент из temp_form_recipient_data"""
    temp_form_recipient_data.pop(user_id, None)


def temp_mem_for_form_creator_remove_form(user_id: int):
    """ Убирает 1 форму из temp_mem_for_form_creator"""
    temp_mem_for_form_creator.pop(user_id, None)


def temp_mem_for_form_creator_remove_form_element(user_id: int, delete_id: int):
    """ Убирает 1 элемент формы по delete_id из temp_mem_for_form_creator"""
    temp_mem_for_form_creator[user_id].pop(delete_id, None)


def mem_for_created_forms_delete_question(form_id: int, question_id: int):
    """ (Для БД) Убирает 1 элемент формы по question_id из mem_for_created_forms"""
    """ form_id - айди формы, question_id - айди вопроса"""
    """ 
        Пример data:
    [{'question': 'opros', 'options': ['helicopter ', ' paracopter'], 'message_id': 0, 'type': 'poll'}, {'question': 'klava', 'message_id': 0, 'type': 'msg'}, {'form_name': 'formo', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}]
        
        Пример mem_for_created_forms:
        {*form_id*: [form data], ...}
    """
    
    # if form_id in mem_for_created_forms.keys():
    #     mem_for_created_forms[form_id].pop(question_id)
    db_mem_for_created_forms_delete_question(form_id, question_id)


def mem_for_created_forms_delete_form(form_id: int):
    """ (Для БД) Убирает 1 форму из mem_for_created_forms"""
    """ form_id - айди формы"""
    # mem_for_created_forms.pop(form_id, None)
    db_mem_for_created_forms_delete_form(form_id)


def completing_forms_dispatcher_remove_session(user_id: int):
    """ Убирает 1 активную сессию  из completing_forms_dispatcher"""
    completing_forms_dispatcher.pop(user_id, None)
    

def registerData_remove_user(user_id: int):
    """ (Для БД) Убирает запись о регистрации пользователя из registerData"""
    """ user_id - айди пользователя"""
    # registerData.pop(user_id, None)
    db_registerData_remove_user(user_id)
#  --- дальше забей ---

def edited_register_data_remove_user(user_id: int):
    edited_register_data.pop(user_id, None)


def choosing_groups_dispatcher_remove_user(user_id: int):
    if user_id in choosing_groups_dispatcher.keys():
        choosing_groups_dispatcher.pop(user_id, None)


def choosing_groups_dispatcher_remove_poll(user_id: int, poll_id: int):
    if user_id in choosing_groups_dispatcher.keys():
        for form_id in choosing_groups_dispatcher[user_id]:
            if choosing_groups_dispatcher[user_id][form_id]['poll_id'] == poll_id:
                choosing_groups_dispatcher[user_id].pop(form_id, None)
                break # ругается
        print(choosing_groups_dispatcher)


def chosen_groups_data_remove_user(user_id: int):
    if user_id in temp_chosen_groups_data.keys():
        temp_chosen_groups_data.pop(user_id, None)


def temp_form_index_data_remove_index(user_id: int):
    temp_form_index_data.pop(user_id, None)
