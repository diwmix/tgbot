from aiogram import Dispatcher, Bot, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
import random
import json
from datetime import datetime

from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from config import TOKEN

with open('result.json', 'r', encoding='utf-8') as file:
    stickers = json.load(file)

telegram_bot = Bot(TOKEN)
dispatcher = Dispatcher(telegram_bot, storage=MemoryStorage())

start_keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton('Карта Дня ☀️'), KeyboardButton('Так чи ні 🌓')]],
    resize_keyboard=True
)


class Form(StatesGroup):
    text = State()

# При Старті
@dispatcher.message_handler(commands=['start'])
async def start_handler(message: Message) -> None:
    await message.answer('Виберіть дію:', reply_markup=start_keyboard)


# При натисненні на скасувати
@dispatcher.message_handler(Text(equals='Скасувати 🚫', ignore_case=True), state='*')
async def cancel_state(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state is None:
        return

    await state.finish()
    await message.answer('Виберіть дію:', reply_markup=start_keyboard)


# Карта дня - таймер
def is_timestamp_relevant(
        timestamp: float,
        now: datetime,
        seconds: int = 86400
) -> None:

    if not timestamp:
        return True

    return (now - datetime.fromtimestamp(timestamp)).total_seconds() > seconds


# При натисненны на карта дня
@dispatcher.message_handler(commands=['Card_Of_The_Day'])
@dispatcher.message_handler(Text(equals='Карта Дня ☀️'))
async def card_of_day(message: Message, state: FSMContext) -> None:

    async with state.proxy() as data:
        last_ping = data.get('last_used')
        now = datetime.now()

        if not is_timestamp_relevant(last_ping, now):
            return await message.answer('Не минуло 24 години! 🕑')

        data['last_used'] = now.timestamp()

    random_sticker = random.choice(stickers)

    with open(random_sticker['sticker_path'], 'rb') as sticker:
        await message.answer_sticker(sticker)

    await message.answer(f"<b>Карта дня:</b>\n\n{random_sticker['sticker_text']}", parse_mode='html')

# При натисненні на "так чи ні"
@dispatcher.message_handler(commands=['Yes_Or_Not'])
@dispatcher.message_handler(Text(equals='Так чи ні 🌓', ignore_case=True))
async def button_2_pattern(message: Message) -> None:
    await Form.text.set()

    await message.answer(
        '<b>Задай Питання!</b>💡\n(Питання треба сформулювати так, щоб на нього можна було дати відповідь "Так" або "Ні".',
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton('Скасувати 🚫')]],
            resize_keyboard=True
        ), parse_mode='html'
    )


@dispatcher.message_handler(state=Form.text)
async def text_state(message: Message, state: FSMContext) -> None:
    await state.finish()
    random_sticker = random.choice(stickers)

    with open(random_sticker['sticker_path'], 'rb') as sticker:
        await message.answer_sticker(sticker)


    await message.answer(
        f"<b>Питання:</b> \n\n{message.text}\n\n<b>Відповідь:</b>\n\n{random_sticker['card_value']}" ,
        parse_mode='html',
        reply_markup=start_keyboard
    )


if __name__ == '__main__':
    executor.start_polling(dispatcher)