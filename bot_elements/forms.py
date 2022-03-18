""" Система опросов"""

""" Создается форма, добавляется в хранилище форм"""

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

unique_form_id = 0

from bot_elements.storages.all_storages import temp_form_recipient_data, temp_mem_for_form_creator, mem_for_created_forms, send_forms_mem, completing_forms_dispatcher

from bot_elements.getter.all_getters import temp_form_recipient_data_get_data, temp_mem_for_form_creator_get_data
from bot_elements.setter import all_setters

bot = Bot(token='5110094448:AAGG_IiPPyjvwtROrBqGu0C74EMSjew3NDQ')


async def display_current_temp_mem_status(message: types.Message):
    form_mem = temp_mem_for_form_creator_get_data(user_id=message.chat.id)
    print('form_mem ', form_mem)
    recip_mem = temp_form_recipient_data_get_data(user_id=message.chat.id)
    print('recip_mem ', recip_mem)
    parsed_msg = "name: " + recip_mem['form_name'] + \
        ' ' + 'form_id: ' + str(recip_mem['form_id']) + "\n"
    if form_mem:
        question_number = 0
        for inside_mem in form_mem:
            if inside_mem['type'] == 'poll':
                parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] + ' ' + '['+', '.join(
                    str(e) for e in inside_mem['options']) + ']' + ' ' + '/del' + str(question_number) + '\n')

            elif inside_mem['type'] == 'msg':
                parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] +
                                  ' ' + '/del' + str(question_number) + '\n')

            question_number += 1

        await message.answer(parsed_msg, reply_markup=types.ReplyKeyboardRemove())


class name(StatesGroup):
    """ FSM для выбора названия опроса"""
    waiting_for_name = State()


class form(StatesGroup):
    """ FSM для добавления одного вопроса/ опроса в форму"""

    waiting_for_question = State()
    waiting_for_options = State()


async def choose_name(message: types.Message, state: FSMContext):
    """ Предлагает выбрать название формы"""

    await message.reply("Выберите название формы")
    await name.waiting_for_name.set()


async def choose_type(message: types.Message, state: FSMContext):  # name.waiting_for_name
    """ Запоминает название и предлагает выбрать тип первого добавляемого вопроса"""
    global unique_form_id

    all_setters.temp_form_recipient_data_add_user_data(chat_id=message.chat.id, 
    form_name=str(message.text), type="info", form_id=unique_form_id, creator_id=message.chat.id)

    unique_form_id += 1

    buttons = [
        types.InlineKeyboardButton(
            text="Опрос", callback_data="question_type_poll"),
        types.InlineKeyboardButton(
            text="Ввод с клавы", callback_data="question_type_msg")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await message.reply("Выберите тип вопроса", reply_markup=keyboard)
    await state.finish()


async def get_question(message: types.Message, state: FSMContext):
    """ Получает текст вопроса и тип, затем ЗАПОМИНАЕТ (и предлагает ввести варианты ответов)
        и предлагает добавить вопрос"""

    question = message.text
    await state.update_data(question=question)
    data = await state.get_data()
    if data['type'] == 'msg':

        all_setters.temp_mem_for_form_creator_add_element(user_id=message.chat.id, data={'question': data['question'], 'message_id': 0, 'type': 'msg'})

        print('temp_mem_for_form_creator', temp_mem_for_form_creator)
        buttons = [
            types.InlineKeyboardButton(
                text="Да", callback_data="add_quest_true"),
            types.InlineKeyboardButton(
                text="Нет", callback_data="add_quest_false")
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        await display_current_temp_mem_status(message)

        await message.reply('Добавить ещё 1 вопрос?', reply_markup=keyboard)
        await state.finish()

    else:
        await state.update_data(question=question)
        await message.reply('Пришлите варианты ответов через запятую')
        await form.waiting_for_options.set()


async def get_options(message: types.Message, state: FSMContext):
    """ Получает варианты ответов, ЗАПОМИНАЕТ и предлагает добавить вопрос"""

    options = message.text.split(',')
    await state.update_data(options=options)

    user_data = await state.get_data()
    # print(user_data['question'], user_data['options'])

    all_setters.temp_mem_for_form_creator_add_element(user_id=message.chat.id, data={'question': user_data['question'], 'options': user_data['options'], 'message_id': 0, 'type': 'poll'})
    
    print('temp_mem_for_form_creator', temp_mem_for_form_creator)

    buttons = [
        types.InlineKeyboardButton(text="Да", callback_data="add_quest_true"),
        types.InlineKeyboardButton(
            text="Нет", callback_data="add_quest_false")
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await display_current_temp_mem_status(message)

    await message.reply('Добавить ещё 1 вопрос?', reply_markup=keyboard)
    # print(temp_mem_for_multiple_poll)
    await state.finish()


# callback queries handlers

async def add_quest_true(call: types.CallbackQuery):
    """ Выбор параметров для нового вопроса"""

    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    buttons = [
        types.InlineKeyboardButton(
            text="Опрос", callback_data="question_type_poll"),
        types.InlineKeyboardButton(
            text="Ввод с клавы", callback_data="question_type_msg")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await call.message.reply('Выберите тип вопроса', reply_markup=keyboard)


async def add_quest_false(call: types.CallbackQuery):
    """ Заканчивает создание формы"""

    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await display_current_temp_mem_status(call.message)


    all_setters.temp_mem_for_form_creator_add_element(user_id=call.message.chat.id, data=temp_form_recipient_data[call.message.chat.id].copy())

    all_setters.mem_for_created_forms_add_element(user_id=temp_form_recipient_data[call.message.chat.id]['form_id'], data=temp_mem_for_form_creator[call.message.chat.id].copy())

    print('mem_for_created_forms ', mem_for_created_forms)

    temp_mem_for_form_creator.pop(call.message.chat.id, None)
    temp_form_recipient_data.pop(call.message.chat.id, None)

    print('temp_form_recipient_data ', temp_form_recipient_data)

    await call.message.answer('Форма создана', reply_markup=types.ReplyKeyboardRemove())


async def question_type_poll(call: types.CallbackQuery, state: FSMContext):
    """ Начало создания опроса"""

    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await state.update_data(type='poll')
    await call.message.answer('Введите вопрос', reply_markup=types.ReplyKeyboardRemove())
    await form.waiting_for_question.set()


async def question_type_msg(call: types.CallbackQuery, state: FSMContext):
    """ Начало создания обычного вопроса"""
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await state.update_data(type='msg')
    await call.message.answer('Введите вопрос', reply_markup=types.ReplyKeyboardRemove())
    await form.waiting_for_question.set()


async def del_handler(message: types.Message):
    """Удаляет одну запись из списка temp_mem по её идентификатору"""

    delete_id = int(message.text[4:])
    temp_mem_for_form_creator[message.chat.id].pop(delete_id)
    await message.answer('удалил пункт ' + str(delete_id), reply_markup=types.ReplyKeyboardRemove())
    await display_current_temp_mem_status(message)


def register_handlers_forms(dp: Dispatcher):
    dp.register_message_handler(choose_name, commands="multi_form", state="*")

    dp.register_message_handler(choose_type, state=name.waiting_for_name)
    dp.register_message_handler(get_question, state=form.waiting_for_question)
    dp.register_message_handler(get_options, state=form.waiting_for_options)

    dp.register_callback_query_handler(
        add_quest_true, text="add_quest_true")
    dp.register_callback_query_handler(
        add_quest_false, text="add_quest_false")
    dp.register_callback_query_handler(
        question_type_poll, text="question_type_poll")
    dp.register_callback_query_handler(
        question_type_msg, text="question_type_msg")

    dp.register_message_handler(
        del_handler, lambda message: message.text.startswith('/del'))