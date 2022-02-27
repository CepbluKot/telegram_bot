from msilib import type_key
from db_connect import DataConnect
import json

import sys
sys.path.append('C:\\Users\\ИЛЮХА-БОСС\\Desktop\\Прога\\Python\\telegram_bot')
import full_pars as fl


db = DataConnect()

def correct_str(t_item):
    t_item = "'" + t_item +"'" 
    return t_item 

def add_us(id_us, role):
    id_us = correct_str(str(id_us))

    id_us_ck = db.select_db_where('global_tb', ['id'], ['gl_teleg_id'] ,[id_us],'check')
    if id_us_ck:
        db.insert_db('global_tb', ['gl_teleg_id'], [id_us])

def add_lesson(name_lesson):
    name_lesson = correct_str(str(name_lesson))

    lesson_ck = db.select_db_where('lesson_tb', ['id'], ['lesson_name'] ,[name_lesson],'check')
    if lesson_ck:
        db.insert_db('lesson_tb', ['lesson_name'], [name_lesson])


def add_prepod(name_prepod, id_us_tg):
    name_prepod = correct_str(str(name_prepod))

    prepod_ck = db.select_db_where('teach_tb', ['id'], ['teach_name'], [name_prepod], 'check')
    if prepod_ck:
        db.insert_db('teach_tb', ['teach_name'], [name_prepod])


def add_group(name_group, status):
    name_group = correct_str(str(name_group))
    status = correct_str(str(status))

    if db.select_db_where('group_tb', ['id'], ['group_name', 'group_approved']  ,[name_group, status], 'check'):
        db.insert_db('group_tb', ['group_name', 'group_approved'] , [name_group, status])


def add_student(name_student, teleg_id, name_group):
    name_student = correct_str(str(name_student))
    con_data =[name_student, find_id_group(name_group)]

    if db.select_db_where('student_tb', ['id'], ['student_name', 'group_id' ]  ,con_data, 'check'):
        con_data.append(find_id_global(teleg_id))
        db.insert_db('student_tb', ['student_name', 'group_id', 'gl_id'], con_data)


def add_group_from_json():
    with open('approved_group.json','r', encoding='utf-8') as file:
        apr_group = json.load(file)

        for item in apr_group:
            print(item)
            add_group(correct_str(item), str(apr_group[item]))
        

def find_id_group(name_group):
    name_group = correct_str(str(name_group))
    return str(db.select_db_where('group_tb', ['id'], ['group_name'], [name_group], 'where')[0][0])


def find_id_lesson(name_lesson):
    name_lesson = correct_str(str(name_lesson))
    return str(db.select_db_where('lesson_tb', ['id'], ['lesson_name'], [name_lesson], 'where')[0][0])


def find_id_teach(name_teach):
    name_teach = correct_str(str(name_teach))
    return str(db.select_db_where('teach_tb', ['id'], ['teach_name'], [name_teach], 'where')[0][0])


def find_id_global(teleg_id):
    teleg_id = correct_str(str(teleg_id))
    return str(db.select_db_where('global_tb', ['id'], ['gl_teleg_id'], [teleg_id], 'where')[0][0])

#для проверки одобренности группы
"""
def _group_cheack_approved(name_group):
    with open('approved_group.json','r', encoding='utf-8') as file:
        apr_group = json.load(file)

        try:
            status = apr_group[name_group]
            return status
        except KeyError:
            return False
"""

def connect_gr_th(name_group, t_item):
    con_data = [find_id_group(name_group), find_id_teach(t_item['prepod']), find_id_lesson(t_item['lesson']), t_item['role']]
    
    name_group = correct_str(str(name_group))
    t_item['role'] = correct_str(str(t_item['role']))
    t_item['lesson'] = correct_str(str(t_item['lesson']))
    t_item['prepod'] = correct_str(str(t_item['prepod']))

    if db.select_db_where('connect_tb', ['id'], ['group_id','teach_id', 'lesson_id', 'teach_role'], con_data, 'check'):
        db.insert_db('connect_tb', ['group_id','teach_id', 'lesson_id', 'teach_role'], con_data)
    

def data_for_group(name_group,t_item):
    add_lesson(t_item['lesson'])
    add_prepod(t_item['prepod'])

    connect_gr_th(name_group,t_item)


def data_for_prepod(t_item):
    add_group(t_item['group'])
    add_lesson(t_item['lesson'])
    
    connect_gr_th(t_item['group'], t_item)


def start_pr(name_prepod):
    data = fl.parse_prepod(name_prepod)

    for item in data:
        data_for_prepod(item)


def start_gr(name_group):
    data = fl.parse_group(name_group)
    name_group = correct_str(name_group)

    for item in data:
        data_for_group(name_group, item)