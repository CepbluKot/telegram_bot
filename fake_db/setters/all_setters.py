import json
from fake_db.run_to_create_tables import registerData, mem_for_created_forms, send_forms_mem, engine, forms_answers_mem
from sqlalchemy import insert, update, select
import psycopg2
from bots import student_bot


def db_confirm_user(user_id: int):
    query = update(registerData).where(
        registerData.c.telegram_id == str(user_id)
    ).values(
        confirmed = True
    )

    engine.execute(query)


def db_registerData_add_user(user_id: int, chosen_fio: str, chosen_group: str, chosen_role: str):
    # 'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': False
    query = registerData.insert().values(
        chosen_fio = chosen_fio, 
        chosen_group = chosen_group, 
        chosen_role = chosen_role, 
        telegram_id = str(user_id),
        confirmed = False
    )

    engine.execute(query)


def db_registerData_change_data(user_id: int, chosen_fio: str, chosen_group: str, chosen_role: str):
   
    query = update(registerData).where(
        registerData.c.telegram_id == str(user_id)
    ).values(
        chosen_fio = chosen_fio,
        chosen_group = chosen_group,
        chosen_role = chosen_role,
        confirmed = True
    )

    engine.execute(query)


def db_mem_for_created_forms_add_element(form_id: int, data):
    """ 
        Пример data:
    [{'question': 'opros', 'options': ['helicopter ', ' paracopter'], 'message_id': 0, 'type': 'poll'}, {'question': 'klava', 'message_id': 0, 'type': 'msg'}, {'form_name': 'formo', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}]
        
        Пример mem_for_created_forms:
        {*form_id*: [form data], ...}
    """
    query = mem_for_created_forms.insert().values(
        form_id = form_id,
        form_data = data
    )

    engine.execute(query)


def db_mem_for_created_forms_insert_question(form_id: int, inser_after_id: int, data):
    query = select([mem_for_created_forms]).where(
        mem_for_created_forms.c.form_id == form_id
    )
    
    mem_for_created_forms_copy = engine.execute(query).fetchall()[0][1]

    

    mem_for_created_forms_copy.insert(inser_after_id + 1, data[0])
    query = update(mem_for_created_forms).where(
        mem_for_created_forms.c.form_id == form_id
    ).values(
        form_id = form_id,
        form_data = mem_for_created_forms_copy
    )
    engine.execute(query)
    

def db_mem_for_created_forms_set_new_form_name(form_id: int, new_form_name: str):
    """ 
        Пример mem_for_created_forms[form_id][-1]:
    {'form_name': 'formo', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}
    """
    query = select([mem_for_created_forms]).where(
        mem_for_created_forms.c.form_id == form_id
    )
    mem_for_created_forms_copy = engine.execute(query).fetchall()[0][1]
    mem_for_created_forms_copy[-1]['form_name'] = new_form_name
    query = update(mem_for_created_forms).where(
        mem_for_created_forms.c.form_id == form_id
    ).values(
        form_id = form_id,
        form_data = mem_for_created_forms_copy
    )
    engine.execute(query)


def db_mem_for_created_forms_set_new_question_name(form_id: int, question_id: int, new_question_name: str):
    """ 
        Пример mem_for_created_forms[form_id][question_id]:
    {'question': 'opros', 'options': ['helicopter ', ' paracopter'], 'message_id': 0, 'type': 'poll'}
    """
    query = select([mem_for_created_forms]).where(
        mem_for_created_forms.c.form_id == form_id
    )
    mem_for_created_forms_copy = engine.execute(query).fetchall()[0][1]
    mem_for_created_forms_copy[question_id]['question'] = new_question_name
    query = update(mem_for_created_forms).where(
        mem_for_created_forms.c.form_id == form_id
    ).values(
        form_id = form_id,
        form_data = mem_for_created_forms_copy
    )
    engine.execute(query)

  
def db_mem_for_created_forms_edit_poll_options(form_id: int, question_id: int, new_poll_options: list):
    """ 
        Пример mem_for_created_forms[form_id][question_id]:
    {'question': 'opros', 'options': ['helicopter ', ' paracopter'], 'message_id': 0, 'type': 'poll'}
    """
    query = select([mem_for_created_forms]).where(
        mem_for_created_forms.c.form_id == form_id
    )
    mem_for_created_forms_copy = engine.execute(query).fetchall()[0][1]
    mem_for_created_forms_copy[question_id]['options'] = new_poll_options
    query = update(mem_for_created_forms).where(
        mem_for_created_forms.c.form_id == form_id
    ).values(
        form_id = form_id,
        form_data = mem_for_created_forms_copy
    )
    engine.execute(query)
    

def db_send_forms_mem_add_sent_form(sent_form_id: int, form_id: int, form_creator_user_id: int, send_to_users_ids: list, groups: list):
    """
        Пример send_forms_mem:
    {'sent_form_id': {'form_id': *form_id*, 'info': {'form_creator_user_id': id,'send_to_users_ids': [айдишники], 'send_to_groups': [groups],'got_answers_from': [айдишники]}, ...}
    """
    query = send_forms_mem.insert().values(
        sent_form_id = sent_form_id, 
        form_data = {'form_id': form_id, 'info': {'form_creator_user_id': form_creator_user_id, 'send_to_users_ids': send_to_users_ids, 'send_to_groups': groups, 'got_answers_from': []}}, 
        got_answers_from = []
    )

    print('\n\n this one ',{'form_id': form_id, 'info': {'form_creator_user_id': form_creator_user_id, 'send_to_users_ids': send_to_users_ids, 'send_to_groups': groups, 'got_answers_from': []}}, )

    engine.execute(query)


async def db_send_forms_mem_add_completed_user(sent_form_id: int, user_id: int):
    """
        Пример send_forms_mem[sent_form_id]['info']:
    {'form_creator_user_id': id,'send_to_users_ids': [айдишники], 'send_to_groups': [groups],'got_answers_from': [айдишники]}
    """
    query = select([send_forms_mem]).where(
        send_forms_mem.c.sent_form_id == sent_form_id
    )
    result = engine.execute(query).fetchall()

    if result and user_id in result[0][2]:
        await student_bot.send_message(chat_id=user_id, text='Вы уже проходили данную форму ранее')
        return

    conn = psycopg2.connect(database="testdb", user="postgres",
    password="752505", host="localhost", port=5432)
    cur = conn.cursor()

    print('\n\nfkof ', "UPDATE send_forms_mem SET got_answers_from = array_append(got_answers_from, '{}') where sent_form_id = {};".format(str(user_id), int(sent_form_id)))

    cur.execute("UPDATE send_forms_mem SET got_answers_from = array_append(got_answers_from, '{}') where sent_form_id = {};".format(str(user_id), int(sent_form_id)))
    conn.commit()

    query = select([send_forms_mem]).where(
        send_forms_mem.c.sent_form_id == sent_form_id
    )
    result = engine.execute(query).fetchall()

    completed_users = result[0][2]
    form_copy = result[0][1]

    print('\n\n mate ', form_copy, completed_users)
    form_copy['info']['got_answers_from'] = completed_users

    query = update(send_forms_mem).where(
        send_forms_mem.c.sent_form_id == sent_form_id
    ).values(
        form_data = form_copy
    )
    # result = engine.execute(query).fetchall()
    engine.execute(query)

    # cur.execute("UPDATE send_forms_mem SET form_data = ARRAY [{}] where sent_form_id = {};".format(send_users, int(sent_form_id)))
    # conn.commit()


def db_insert_to_forms_answers_mem(sent_form_id: int, competed_by_user_id: str, form_answers, form_id):
    query = forms_answers_mem.insert().values(
        form_id= form_id,
        sent_form_id = sent_form_id,
        competed_by_user_id = competed_by_user_id,
        form_answers = json.dumps( str(form_answers))
    )

    engine.execute(query)
