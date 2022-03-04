from numpy import delete
import us_init

def update_us(tg_id):
    find_tg_role = us_init.db.select_db_where('global_tb', ['gl_role'], ['gl_teleg_id'], [us_init.correct_str(str(tg_id))], 'where')[0]

    if find_tg_role != (0,):
        us_init.db.delete_db(find_tg_role + '_tb', ['gl_id'], [us_init.find_id_global(tg_id)])
        us_init.db.delete_db('global_tb', ['gl_teleg_tb'], [find_tg_role])
    else:
        print(tg_id, 'не существует!!!!!!!')

def poll_strat():
    pass


def student_start(name_user, id_us_tg,name_group):
    us_init.add_group(name_group, True)
    us_init.add_student(name_user, id_us_tg, name_group)
    #us_init.start_gr(name_group)


def prepod_start(name_user, id_us_tg):
    us_init.add_prepod(name_user, id_us_tg)
    us_init.start_pr(input("введите ссылку на препода: "))


def reg_us(name_user, id_us_tg, role, group_stud = None):
    us_init.add_us(id_us_tg, role)
    print(group_stud, role)

    if role == 'student' and group_stud != None:
        student_start(name_user, id_us_tg, group_stud)
    elif role == 'prepod' and group_stud == None:
        prepod_start(name_user, id_us_tg)


if __name__ == '__main__':
    pass


