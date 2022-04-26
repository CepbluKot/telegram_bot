from django.dispatch import receiver
from fake_db.run_to_create_tables import registerData, mem_for_created_forms, send_forms_mem, engine
from sqlalchemy import update, select
import psycopg2


def db_mem_for_created_forms_get():
    """ (Для БД) Возвращает mem_for_created_forms"""
    """
        Пример mem_for_created_forms:
    {0: [{'question': 'Сос', 'options': ['Лан', ' все'], 'message_id': 0, 'type': 'poll'}, {'question': 'Месяц', 'message_id': 0, 'type': 'msg'}, {'form_name': 'Формо', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}], 1: [{'question': 'Зе криэтир', 'options': ['Один', ' два'], 'message_id': 0, 'type': 'poll'}, {'form_name': 'Тайлер', 'type': 'info', 'form_id': 1, 'creator_id': 506629389}]}
    """

    formatirovanie = {}

    query = select([mem_for_created_forms])
    recieved = engine.execute(query).fetchall()

    for selected_form in recieved:
        id = selected_form[0]
        data = selected_form[1]

        if len(data) == 1:
            formatirovanie[id] = [data]
        else:
            formatirovanie[id] = data

    return formatirovanie


def db_mem_for_created_forms_get_data(form_id: int):
    """ (Для БД) Возвращает ячейку памяти хранящую данные созданной формы (mem_for_created_forms)"""
    """
        form_id - айди формы
        Пример mem_for_created_forms[form_id]:
    [{'question': 'Сос', 'options': ['Лан', ' все'], 'message_id': 0, 'type': 'poll'}, {'question': 'Месяц', 'message_id': 0, 'type': 'msg'}, {'form_name': 'Формо', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}]
    """

    query = select([mem_for_created_forms]).where(
        mem_for_created_forms.c.form_id == form_id
    )
    recieved = engine.execute(query).fetchall()
    data = recieved[0][1]

    if len(data) == 1:
            data = [data]
    
    return data


def db_mem_for_created_forms_get_form_name(form_id: int):
    """ (Для БД) Возвращает название созданной формы из mem_for_created_forms"""
    """
        form_id - айди формы
        Пример mem_for_created_forms[form_id][-1]:
    {'form_name': 'Формо', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}
    """

    query = select([mem_for_created_forms]).where(
        mem_for_created_forms.c.form_id == form_id
    )
    recieved = engine.execute(query).fetchall()
    data = recieved[0][1]

    if len(data) == 1:
            data = [data]
    
    return data[-1]['form_name']


def db_mem_for_created_forms_get_creator_id(form_id: int):
    """ (Для БД) Возвращает айди создателя формы из mem_for_created_forms"""
    """
        form_id - айди формы
        Пример mem_for_created_forms[form_id][-1]:
    {'form_name': 'Формо', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}
    """

    query = select([mem_for_created_forms]).where(
        mem_for_created_forms.c.form_id == form_id
    )
    recieved = engine.execute(query).fetchall()
    data = recieved[0][1]

    if len(data) == 1:
            data = [data]
    print('\n\n data ', recieved)
    return data[-1]['creator_id']



def db_registerData_get():
    """ (Для БД) возвращает registerData"""
    """ 
        Пример registerData:
    {user_id: {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': True/False}, ...}
    """

    formatirovanie = {}

    query = select([registerData])
    recieved = engine.execute(query).fetchall()

    for selected_user in recieved:
        fio = selected_user[1]
        group = selected_user[2]
        role = selected_user[3]
        telegram_id = selected_user[4]
        confirmed = selected_user[5]

        formatirovanie[int(telegram_id)] = {'chosen_fio': fio, 'chosen_group': group, 'chosen_role': role, 'confirmed': confirmed}

    return formatirovanie


def db_registerData_get_fio(user_id: int):
    """ (Для БД) Возвращает ФИО юзера из registerData"""
    """ 
        Пример registerData[user_id]:
    {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': True/False}
    """

    query = select([registerData]).where(
        registerData.c.telegram_id == str(user_id)
    )
    recieved = engine.execute(query).fetchall()

    return recieved[0][1]


def db_registerData_get_group(user_id: int):
    """ (Для БД) Возвращает группу юзера из registerData"""
    """ 
        Пример registerData[user_id]:
    {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': True/False}
    """

    query = select([registerData]).where(
        registerData.c.telegram_id == str(user_id)
    )
    recieved = engine.execute(query).fetchall()

    return recieved[0][2]

def db_registerData_get_role(user_id: int):
    """ (Для БД) Возвращает роль юзера из registerData"""
    """ 
        Пример registerData[user_id]:
    {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': True/False}
    """

    query = select([registerData]).where(
        registerData.c.telegram_id == str(user_id)
    )
    recieved = engine.execute(query).fetchall()

    return recieved[0][3]


def db_registerData_check_is_in_register_list(user_id: int):
    """ (Для БД) Проверяет есть ли юзер в registerData"""

    """ user_id - айди юзера;  (эта функция по факту повторяется, но она нужна)"""

    query = select([registerData]).where(
        registerData.c.telegram_id == str(user_id)
    )
    recieved = engine.execute(query).fetchall()
    return bool(recieved)


def db_registerData_check_is_registered(user_id: int):
    """ (Для БД) Проверяет есть ли юзер в registerData"""
    """ 
        Формат registerData:
        {user_id: {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': False}, ...}
    """

    query = select([registerData]).where(
        registerData.c.telegram_id == str(user_id)
    )
    recieved = engine.execute(query).fetchall()
    print('register ', recieved)
    if bool(recieved):
        return recieved[0][-1]
    
    return False


def db_registerData_check_is_confirmed(user_id: int):
    """ (Для БД) Проверяет подтвержден ли юзер в registerData"""

    """ user_id - айди юзера"""
    """ 
        Пример registerData[user_id]:
    {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': True/False}
    """

    query = select([registerData]).where(
        registerData.c.telegram_id == str(user_id)
    )
    recieved = engine.execute(query).fetchall()

    if bool(recieved):
        return recieved[0][-1]


def db_send_forms_mem_get():
    """ (Для БД) Возвращает send_forms_mem (память с отправленынми формами)"""
    """ 
    Формат send_forms_mem
    {'sent_form_id': {'form_id': *form_id*, 'info': {'form_creator_user_id': id,'send_to_users_ids': [ids], 'got_answers_from': [ids]}, ...} 
    """

    formatirovanie = {}

    query = select([send_forms_mem])
    recieved = engine.execute(query).fetchall()


    for selected_form in recieved:
        sent_form_id = selected_form[0]
        form_data = selected_form[1]

        formatirovanie[sent_form_id] = form_data
    
    return formatirovanie


def db_send_forms_mem_get_form(sent_form_id: int):
    """ (Для БД) Возвращает форму из send_forms_mem (память с отправленынми формами)"""

    """ sent_form_id - айди отправленной формы"""

    """ 
    Формат send_forms_mem[sent_form_id]
    {'form_id': *form_id*, 'info': {'form_creator_user_id': id,'send_to_users_ids': [айдишники], 'got_answers_from': [айдишники]}}
    """

    query = select([send_forms_mem]).where(
        send_forms_mem.c.sent_form_id == sent_form_id
    )
    recieved = engine.execute(query).fetchall()
    data = (recieved[0][1])
    
    return data


def db_send_forms_mem_get_form_sent_users(sent_form_id: int):
    """ (Для БД) Возвращает айди пользователей, которым отослана форма"""

    """ sent_form_id - айди отправленной формы"""

    """ 
    Формат send_forms_mem[sent_form_id]['info']
    {'form_creator_user_id': id,'send_to_users_ids': [айдишники], 'got_answers_from': [айдишники]}
    """

    query = select([send_forms_mem]).where(
        send_forms_mem.c.sent_form_id == sent_form_id
    )
    recieved = engine.execute(query).fetchall()
    data = (recieved[0][1])

    return data['info']['send_to_users_ids']


def db_send_forms_mem_get_form_completed_users(sent_form_id: int):
    """ (Для БД) Возвращает айди пользователей, которые прошли форму"""

    """ sent_form_id - айди отправленной формы"""

    """ 
    Формат send_forms_mem[sent_form_id]['info']
    {'form_creator_user_id': id,'send_to_users_ids': [айдишники], 'got_answers_from': [айдишники]}
    """

    query = select([send_forms_mem]).where(
        send_forms_mem.c.sent_form_id == sent_form_id
    )
    recieved = engine.execute(query).fetchall()
    data = (recieved[0][1])

    return data['info']['got_answers_from']


def db_unique_form_id_get():
    """ (Для БД) Возвращает счетчик созданных форм"""
    # print(' \n\nloool unique_form_id ', bot_elements.storages.all_storages.unique_form_id)
    query = select([send_forms_mem])
    recieved = engine.execute(query).fetchall()
    return (recieved[-1][1]['form_id'])


def db_unique_sent_form_id_get():
    """ (Для БД) Возвращает счетчик отправленных форм"""
    # print('unique_sent_form_id ',bot_elements.storages.all_storages.unique_sent_form_id)
    # return bot_elements.storages.all_storages.unique_sent_form_id
    query = select([send_forms_mem])
    recieved = engine.execute(query).fetchall()
    return (recieved[-1][0])


def db_get_all_groups():
    """ (Для БД) Возвращает список всех групп"""
    all_groups = ['М3О-212Б-20', 'М3О-214Б-20', 'М3О-309Б-19', 'М3О-314Б-19', 'М3О-118М-21',
              'М3О-111М-21',  'М3О-214Б-20', 'М3О-221Б-20', 'М3О-309Б-19', 'М3О-314Б-19']

    return all_groups


def db_get_group_users_ids(groups: list):
    """ (Для БД) Возвращает список айдишников студентов из выбранных групп"""
    """ groups - список с группами"""

    return [506629389]


def db_get_document(form_id: int, sent_form_id: int): # Илья сюда
    """ (Для БД) Возвращает pdf документ с результатом формы"""
    """ form_id - айдишник формы, sent_form_id - айдишник отправленной формы"""

    pass
