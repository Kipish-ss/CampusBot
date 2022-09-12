import math
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import df, PART_URL
from .callbacks_data import names_callback, subjects_callback


def get_names_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=4)
    surnames = df['Full Name'].apply(lambda x: x.split()[0])
    for i in range(df.shape[0]):
        keyboard.insert(InlineKeyboardButton(surnames[i], callback_data=names_callback.new(action='show', index=i)))
    keyboard.row(InlineKeyboardButton('Close❌', callback_data=names_callback.new(action='close', index='')))
    return keyboard


def get_subjects_keyboard(subjects, subjects_links, index):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for i in range(len(subjects)):
        keyboard.insert(InlineKeyboardButton(subjects[i], callback_data=subjects_callback.new(
            act='show',
            link=subjects_links[i].replace(PART_URL, ''),
            index=index)))
    keyboard.row(InlineKeyboardButton(text='Back👈', callback_data=subjects_callback.new(act='return',
                                                                                           link='', index='')))
    return keyboard
