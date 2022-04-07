""" Статус пользователя"""
from aiogram import Dispatcher, types
from bot_elements.getter.all_getters import get_document, mem_for_created_forms_get_form_name, send_forms_mem_get



async def display_user_status(message: types.Message):

    full_message = "Отправленные вами формы:"

    for sent_form_id in send_forms_mem_get():
        form = send_forms_mem_get()
        select_form = form[sent_form_id]
        if message.chat.id == select_form['info']['form_creator_user_id']:
            
            send_to = select_form['info']['send_to_users_ids']
            completed_by = select_form['info']['got_answers_from']
            form_id = select_form['form_id']

            if send_to and completed_by:

                full_message +=  '\n' + 'НАЗВАНИЕ: ' + str(mem_for_created_forms_get_form_name(form_id)) + ' ПРОЦЕСС ВЫПОЛНЕНИЯ: ' + str(len(send_to) / len(completed_by)) + ' % (' + str(len(send_to)) + ' / ' + str(len(completed_by)) + '/getResult_' + form_id + '_' + sent_form_id
            
            else:
                full_message +=  '\n' + ' Ошибка при обработке опроса (неверно заданы получатели)'  

    if full_message == "Отправленные вами формы:":
        await message.answer('Вы не создали ни одной формы')

    else:
        await message.answer(full_message)


def get_form_result(message: types.Message):
    indexes = message[11:].split('_')
    form_id = indexes[0]
    sent_form_id = indexes[1]

    doc = get_document()
    # message.answer_document()
    message.answer('тут должен отправиться документ')


def register_handlers_prepod_status(dp: Dispatcher):

    dp.register_message_handler(
        display_user_status, commands="status", state="*")
    dp.register_message_handler(
        get_form_result, lambda message: message.text.startswith('/getResult_'))
