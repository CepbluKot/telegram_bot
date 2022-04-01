from aiogram import Bot
import json

with open('config.json') as file:
    config = json.load(file)

prepod_bot = Bot(token=config['prepodBotToken'])
student_bot = Bot(token=config['studentBotToken'])
admin_bot = Bot(token=config['adminBotToken'])
adminIds = config['adminIds']
