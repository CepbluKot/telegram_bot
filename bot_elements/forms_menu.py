""" Меню для системы опросов"""
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

unique_sent_form_id = 0

from bot_elements.forms import mem_for_created_forms, send_forms_mem
# check forms mass and select user_ids + send forms in forms.py

async def display_current_mem_status(message: types.Message):
    full_message = ""
    for index in mem_for_created_forms:
        
        if mem_for_created_forms[index][-1]['creator_id'] == message.chat.id:
            selected_form = mem_for_created_forms[index]
            form_mem = selected_form
            print('form_mem ', form_mem)
            info = selected_form[-1]
            print('recip_mem ', info)
            
            parsed_msg = "\n ----- \nname: " + info['form_name'] + ' '+ 'form_id: ' + str(info['form_id']) + ' /send' + '_' + str(index) + "\n"

            if form_mem:
                
                for inside_mem in form_mem:
                    if inside_mem['type'] == 'poll':
                        parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] + ' ' + '['+', '.join(
                            str(e) for e in inside_mem['options']) + ']' + '\n')

                    elif inside_mem['type'] == 'msg':
                        parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] + '\n')

        full_message += parsed_msg
    
    await message.answer(full_message)


#send fsm

class sender(StatesGroup):
    waiting_for_groups = State()


async def choose_group(message: types.Message, state: FSMContext):
    form_index = message.text[6:]

    await state.update_data(form_index=form_index)
    await message.reply('Напишите через запятую группы-получатели')
    await sender.waiting_for_groups.set()


async def sending(message: types.Message, state: FSMContext):
    global unique_sent_form_id

    groups = message.text.split(',')
    final_data = await state.get_data()
    form_creator_user_id = mem_for_created_forms[int(final_data['form_index'])][-1]['creator_id']
    # получить id юзеров по группам
    send_forms_mem.append({'form_id': int(final_data['form_index']), 'sent_form_id': unique_sent_form_id, 'info': {'form_creator_user_id': form_creator_user_id, 'send_to_users_ids': [506629389]}})
    print(send_forms_mem)

    unique_sent_form_id += 1

    await message.answer('Отправлено группам' + ''.join(str(groups)))
    await state.finish()


def register_handlers_forms_menu(dp: Dispatcher):
    dp.register_message_handler(display_current_mem_status, commands="saved_forms", state="*")
    dp.register_message_handler(choose_group, lambda message: message.text.startswith('/send'))
    dp.register_message_handler(sending, state=sender.waiting_for_groups)
