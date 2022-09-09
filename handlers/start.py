from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from utils.logging import get_logger

logger = get_logger()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.reply('Hi')