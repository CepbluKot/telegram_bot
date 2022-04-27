from fake_db.run_to_create_tables import registerData, mem_for_created_forms, send_forms_mem, engine
from sqlalchemy import update, select, delete
import psycopg2



def db_mem_for_created_forms_delete_question(form_id: int, question_id: int):
    """ (Для БД) Убирает 1 элемент формы по question_id из mem_for_created_forms"""
    """ form_id - айди формы, question_id - айди вопроса"""
    """ 
        Пример data:
    [{'question': 'opros', 'options': ['helicopter ', ' paracopter'], 'message_id': 0, 'type': 'poll'}, {'question': 'klava', 'message_id': 0, 'type': 'msg'}, {'form_name': 'formo', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}]
        
        Пример mem_for_created_forms:
        {*form_id*: [form data], ...}
    """
    
    query = select([mem_for_created_forms]).where(
        mem_for_created_forms.c.form_id == form_id
    )
    
    mem_for_created_forms_copy = engine.execute(query).fetchall()[0][1]
    mem_for_created_forms_copy.pop(question_id)
    query = update(mem_for_created_forms).where(
        mem_for_created_forms.c.form_id == form_id
    ).values(
        form_id = form_id,
        form_data = mem_for_created_forms_copy
    )
    engine.execute(query)
    

def db_mem_for_created_forms_delete_form(form_id: int):
    """ (Для БД) Убирает 1 форму из mem_for_created_forms"""
    """ form_id - айди формы"""
    
    query = delete(mem_for_created_forms).where(
        mem_for_created_forms.c.form_id == form_id
    )
    engine.execute(query)


def db_registerData_remove_user(user_id: int):
    """ (Для БД) Убирает запись о регистрации пользователя из registerData"""
    """ user_id - айди пользователя"""
    query = delete([registerData]).where(
        mem_for_created_forms.c.telegram_id == user_id
    )
    engine.execute(query)
