import json
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import requests

# Настройки логирования
logging.basicConfig(level=logging.INFO)

# Токен бота
def load_config() -> dict:
    """Загрузка конфигурации из файла config.json"""
    with open('config.json') as f:
        return json.load(f)

config = load_config()
API_TOKEN = config['API_TOKEN']

# Создание бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Клавиатура
def create_keyboard() -> types.ReplyKeyboardMarkup:
    """Создание клавиатуры"""
    button1 = types.KeyboardButton(text='Старт')
    button2 = types.KeyboardButton(text='Информация')
    button3 = types.KeyboardButton(text='Шутка')
    button4 = types.KeyboardButton(text='Покажи собаку')

    keyboard = [
        [button4,],
        [button3, button2],
        [button1,]
    ]

    return types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

kb1 = create_keyboard()

# Обработчик команды /start
@dp.message(F.text == 'Старт')
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    try:
        name = message.chat.first_name
        await message.answer(f'Привет, {name}! Я бот Вова знаю три слова - /start, /info, /joke и собаку могу показать', reply_markup=kb1)
    except Exception as e:
        logging.error(f'Ошибка при обработке команды /start: {e}')

# Обработчик команды /info
@dp.message(F.text == 'Информация')
@dp.message(Command('info'))
async def cmd_info(message: types.Message):
    """Обработчик команды /info"""
    try:
        await message.reply('Я тестовый бот, не обижайте меня, а то Вам прилетит', reply_markup=kb1)
    except Exception as e:
        logging.error(f'Ошибка при обработке команды /info: {e}')

# Обработчик команды /joke
# Обработчик команды /joke
@dp.message(F.text == 'Шутка')
@dp.message(Command('joke'))
async def cmd_joke(message: types.Message):
    """Обработчик команды /joke"""
    try:
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text='Несите счет', callback_data='yes'),
             types.InlineKeyboardButton(text='Нет', callback_data='no')]
        ])
        await message.answer('Купи слона', reply_markup=keyboard)
    except Exception as e:
        logging.error(f'Ошибка при обработке команды /joke: {e}')

# Обработчик кнопок "Несите счет" и "Нет"
@dp.callback_query()
async def callback_handler(call: types.CallbackQuery):
    """Обработчик кнопок "Несите счет" и "Нет" """
    if call.data == 'yes':
        await call.message.answer('Какой молодец я гениальный продавец!')
        await call.message.answer('Хочешь собаку покажу?'),
    elif call.data == 'no':
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text='Несите счет', callback_data='yes'),
             types.InlineKeyboardButton(text='Нет', callback_data='no')]
        ])
        await call.message.answer('Все говорят нет, а ты купи слона', reply_markup=keyboard)

# Обработчик команды /dog
@dp.message(F.text == 'Покажи собаку')
@dp.message(Command('dog'))
async def cmd_dog(message: types.Message):
    """Обработчик команды /dog"""
    try:
        url = 'https://dog.ceo/api/breeds/image/random'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            image_dog = data.get('message')
            await message.answer_photo(photo=image_dog)
        else:
            await message.reply('Ошибка при загрузке изображения')
    except Exception as e:
        logging.error(f'Ошибка при обработке команды /dog: {e}')

# Обработчик команд реагирующих на сообщения
@dp.message(F.text)
async def msg_echo(message: types.Message):
    """Обработчик команд реагирующих на сообщения"""
    msg_user = message.text.lower()
    name = message.chat.first_name
    if 'привет' in msg_user:
        await message.answer(f'Привет - {name}')
    elif 'пока' in msg_user:
        await message.answer(f'Пока - {name}')
    elif 'кто' in msg_user or 'ты кто' in msg_user:
        await message.answer(f'Я тестовый бот - {name}')
    else:
        await message.answer(f'Я пока не знаю такого слова - {name}')

# Обработчик неизвестных команд
@dp.message()
async def unknown_command(message: types.Message):
    """Обработчик неизвестных команд"""
    try:
        command_list = 'Доступные команды:\n/info\n/joke'
        await message.answer(command_list)
    except Exception as e:
        logging.error(f'Ошибка при обработке неизвестной команды: {e}')

# Основная функция
async def main():
    """Основная функция"""
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f'Ошибка при запуске бота: {e}')

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
