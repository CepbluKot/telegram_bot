from sqlalchemy import ARRAY, MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, JSON, create_engine, select
from datetime import datetime
import json


engine = create_engine("postgresql+psycopg2://postgres:752505@localhost/testdb")
engine.connect()

metadata = MetaData()


registerData = Table('registerData', metadata, 
    Column('id', Integer(), primary_key=True),
    Column('chosen_fio', String(128), nullable=False),
    Column('chosen_group', String(128), nullable=False),
    Column('chosen_role', String(128), nullable=False),
    Column('telegram_id', Text(), nullable=False),
    Column('confirmed', Boolean(), nullable=False)
)


mem_for_created_forms = Table('mem_for_created_forms', metadata,
    Column('form_id', Integer(), nullable=False),
    Column('form_data', JSON(), nullable=False)
)


send_forms_mem = Table('send_forms_mem', metadata, 
    Column('sent_form_id', Integer(), nullable=False),
    Column('form_data', JSON(), nullable=False),
    Column('got_answers_from', ARRAY(Text), nullable=False)
)


forms_answers_mem = Table('forms_answers_mem', metadata, 
    Column('form_id', Integer(), nullable=False),
    Column('sent_form_id', Integer(), nullable=False),
    Column('competed_by_user_id', Text(), nullable=False),
    Column('form_answers', JSON(), nullable=False)
)


metadata.create_all(engine)

# engine.execute(operation)

# res = engine.execute(guys.select())
# mas = res.fetchall()
