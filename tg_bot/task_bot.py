from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
import aiohttp
import json, os

with open('config_bot.json', 'r') as file:
    config = json.load(file)


storage=MemoryStorage()
bot = Bot(token=config['token'])
dp = Dispatcher(bot, storage=storage) 

def get_cancel() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))

class CreateTask(StatesGroup):
    write_name = State()
    write_description = State()

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(
        "Привет! Я бот буду создавать и показывать ваши задачи\n"
        "Для вывола списка задачь /tasks_list\n"
        "Для создания задачи /create_task\n"
        "Приятного пользования"
        )

@dp.message_handler(commands=['cancel'], state='*')
async def cancel_create_task(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.answer(
            'Создание задачи отменено',
            reply_markup = ''
        )
    await state.finish()

@dp.message_handler(commands=['tasks_list'])
async def get_list_tasks(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/teleg/tasks/', json={'username': message.chat.username}) as page:
            data = await page.read()
            data = data.decode().replace("'", '"')
            response = '\n'.join(f'Название: {row["name"]}\nОписание: {row["description"]}' for row in json.loads(data))
            await message.answer(
                f'Список ваших задач:\n{response}'
            )

@dp.message_handler(commands=['create_task'])
async def create_tasks(message: types.Message, state: FSMContext):
    await message.answer(
        text="Напишите название задания:",
        reply_markup=get_cancel()
    )
    await state.set_state(CreateTask.write_name)

@dp.message_handler(state=CreateTask.write_name)
async def task_write_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text="Спасибо. Теперь напишите описание:",
        reply_markup=get_cancel()
    )
    await state.set_state(CreateTask.write_description)

@dp.message_handler(state=CreateTask.write_description)
async def task_write_description(message: Message, state: FSMContext):
    user_data = await state.get_data()
    data = {'username': message.chat.username,
            'name': user_data['name'],
            'description': message.text}
    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8000/teleg/tasks/', json=data) as page:
            status = page.status
            if status == 201:
                await message.answer(
                    'Задача создана'
                )
            elif status == 404:
                await message.answer(
                    'Ваш аккаунт не зарегистрирован'
                )
            else:
                await message.answer(
                    'Увы задача не создалась'
                )
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp)
