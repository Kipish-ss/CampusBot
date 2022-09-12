from aiogram.types import Message, CallbackQuery
from keyboards.inline.callbacks_data import names_callback, subjects_callback
from keyboards.inline.get_inline_keyboards import get_names_keyboard
from loader import dp, bot
from .marks_functions import _confirm_person, _choose_subject, _return_to_person_choice
from message_functions import delete_message


@dp.message_handler(commands='get_marks')
async def choose_person(message: Message):
    await message.reply('Choose the person:', reply_markup=get_names_keyboard())
    await delete_message(message)


@dp.callback_query_handler(names_callback.filter(action='show'))
async def confirm_person(call: CallbackQuery, callback_data: dict):
    await _confirm_person(call, callback_data)


@dp.callback_query_handler(names_callback.filter(action='close'))
async def close_menu(call: CallbackQuery):
    await delete_message(call.message)


@dp.callback_query_handler(subjects_callback.filter(act='show'))
async def choose_subject(call: CallbackQuery, callback_data: dict):
    await _choose_subject(call, callback_data)


@dp.callback_query_handler(subjects_callback.filter(act='return'))
async def return_to_person_choice(call: CallbackQuery):
    await _return_to_person_choice(call)
