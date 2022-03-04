import asyncio
from asyncio import get_event_loop
from aiogram import Dispatcher, types, Bot, executor
import aiogram
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher.filters import Text

import prep_text_pars
import sys
sys.path.append('C:\\Users\\ИЛЮХА-БОСС\\Desktop\\Прога\\Python\\telegram_bot\\db_setting')

import tg_connect_db as tg_db
from us_init import find_teleg_group
from db_connect import DataConnect
from us_init import find_teleg_group


API_TOKEN = '5110094448:AAGG_IiPPyjvwtROrBqGu0C74EMSjew3NDQ'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage(), loop=get_event_loop())
polls_dispcatcher = []


db = DataConnect()
all_groups = []
for data in prep_text_pars.get_prepod_page('https://mai.ru/education/studies/schedule/ppc.php?guid=d0c04806-1d99-11e0-9baf-1c6f65450efa#'):
    all_groups.append(data['group'])

# all_groups = ['blat', 'gfto', 'ayli']

# all_groups = db.select_db('group_tb', ['group_name'])
# all_groups_norm = []
# for data in all_groups:
#     all_groups_norm.append(data[0])


# ############### poll #################

@dp.message_handler(commands=["poll"])
async def cmd_poll(message: types.message):
    await message.answer('Высылаю опрос')
    options = ['MaXImus', 'DmitRUS', 'FedoSUS', 'Ilyxus', 'ArtemOS']
    # chat_id = message.chat.id
    chat_id = message.chat.id
    is_anonymous = True
    # open_period = 10
    question = 'you are'

    poll = await bot.send_poll(options=options, is_anonymous=is_anonymous, question=question, chat_id=chat_id)

    # send chat id and poll id
    polls_dispcatcher.append(
        {"chat_id": poll.chat.id, "message_id": poll.message_id})
    await asyncio.sleep(5)
    count = 0
    for data in polls_dispcatcher:

        res = await bot.stop_poll(chat_id=data['chat_id'], message_id=data['message_id'])
        print(count, '  ', res, data['chat_id'])
        count += 1
    polls_dispcatcher.clear()
    count = 0
    # await asyncio.sleep(1)

# ############## end poll #################


# ################regiser zone #############################

class registerUser(StatesGroup):
    waiting_for_role = State()
    waiting_for_fio = State()
    waiting_for_group = State()


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    print(current_state)
    if current_state is None:
        return
    await state.finish()
    await message.answer('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands='register')
async def choose_role(message: types.Message):

    buttons = [
        types.InlineKeyboardButton(text="Студент", callback_data="is_student"),
        types.InlineKeyboardButton(
            text="Преподаватель", callback_data="is_prepod")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await message.answer("Выберите роль      ", reply_markup=keyboard)


@dp.message_handler(state=registerUser.waiting_for_fio)
async def fio_choosen(message: types.Message, state: FSMContext):
    fio = message.text.lower()
    await message.answer('your fio:' + fio)
    await state.update_data(chosen_fio=fio)
    user_data = await state.get_data()
    if user_data['chosen_role'] == 'student':
        marakap = ReplyKeyboardMarkup()

        for data in all_groups:
            marakap.add(KeyboardButton(data))

        await registerUser.next()
        await message.reply('Выберите группу', reply_markup=marakap)

    else:
        tg_db.reg_us(user_data['chosen_fio'], message.from_user.id, user_data['chosen_role'])

        await message.reply('вы ' + user_data['chosen_fio'] + ' ' + user_data['chosen_role'])
      
# ######################### ############### ##########
        await state.finish()


@dp.message_handler(state=registerUser.waiting_for_group)
async def choose_group(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data['chosen_role'] != "prepod":

        group = message.text

        await state.update_data(chosen_group=group)
        user_data = await state.get_data()
        tg_db.reg_us(user_data['chosen_fio'], message.from_user.id, user_data['chosen_role'], group_stud = user_data['chosen_group'])

        await message.answer(f"{user_data['chosen_role']} {user_data['chosen_group']} {user_data['chosen_fio']}.\n", reply_markup=types.ReplyKeyboardRemove())

# #########################################################

    await state.finish()


@dp.callback_query_handler(text="is_student")
async def is_stud(call: types.CallbackQuery, state: FSMContext):
    await registerUser.waiting_for_role.set()
    await state.update_data(chosen_role="student")
    await call.answer()
    await registerUser.next()
    await call.message.answer('Введите ФИО')


@dp.callback_query_handler(text="is_prepod")
async def is_prep(call: types.CallbackQuery, state: FSMContext):
    await registerUser.waiting_for_role.set()
    await state.update_data(chosen_role="prepod")
    await call.answer()
    # user_data = await state.get_data()
    # await call.message.answer('Вы '+ user_data['chosen_role'])
    await registerUser.next()
    await call.message.answer('Введите ФИО')


# ################ end register ########


# ############## poll creator ###########


async def make_poll(chat_id, options=['NO OPTIONS'], is_anonymous=True, question='NO QUESTION'):

    for recipient in chat_id:
        poll = await bot.send_poll(options=options, is_anonymous=is_anonymous, question=question, chat_id=recipient)

        polls_dispcatcher.append(
            {"chat_id": poll.chat.id, "message_id": poll.message_id})
        await asyncio.sleep(5)
        count = 0
        for data in polls_dispcatcher:

            res = await bot.stop_poll(chat_id=data['chat_id'], message_id=data['message_id'])
            print(count, '  ', res, data['chat_id'])
            count += 1
        polls_dispcatcher.clear()
        count = 0


class createPoll(StatesGroup):
    waiting_for_question = State()
    waiting_for_options = State()
    waiting_for_recipient = State()


@dp.message_handler(commands='create_poll')
async def choose_question(message: types.Message):
    await createPoll.next()
    await message.reply("Введите вопрос")


@dp.message_handler(state=createPoll.waiting_for_question)
async def fio_choosen(message: types.Message, state: FSMContext):

    question = message.text.lower()

    await state.update_data(question=question)
    await message.reply('Пришлите вопросы через запятую')
    await createPoll.next()


@dp.message_handler(state=createPoll.waiting_for_options)
async def fio_choosen(message: types.Message, state: FSMContext):

    options = message.text.split(',')
    await state.update_data(options=options)

    marakap = ReplyKeyboardMarkup()

    for data in all_groups:
        marakap.add(KeyboardButton(data))

    await message.reply('Выберите какой группе отправить', reply_markup=marakap)

    await createPoll.next()


@dp.message_handler(state=createPoll.waiting_for_recipient)
async def fio_choosen(message: types.Message, state: FSMContext):
    group = message.text.lower()

    users_id_list = []
    users_id_list = find_teleg_group(group)


# ############### # ############### # ############### # ############### 
    await state.update_data(group=group)
    user_data = await state.get_data()
    await message.answer('ГОТОВО', reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    await make_poll(chat_id=users_id_list, question=user_data['question'], options=user_data['options'])
    # await make_poll(chat_id=find_teleg_group(group), question=user_data['question'], options=user_data['options'])
    
    

# ################# creatr end #########


async def set_commands():

    commands = [
        BotCommand(command="/create_poll", description="Создать опрос"),
        BotCommand(command="/poll", description="Опрос"),
        BotCommand(command="/register", description="Регистрация"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]

    await bot.set_my_commands(commands)


async def pritr():
    while True:
        await asyncio.sleep(5)


if __name__ == '__main__':

    dp.loop.create_task(set_commands())
    dp.loop.create_task(pritr())
    executor.start_polling(dp)