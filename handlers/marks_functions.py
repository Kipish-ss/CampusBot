from aiogram.utils.exceptions import RetryAfter, MessageNotModified
from data.config import URL, df, data_year, PART_URL, POST_URL, AUTH_URL, SUBJECTS_URL
from message_functions import delete_message
from utils.logging import get_logger
import requests
from bs4 import BeautifulSoup
import aiogram.utils.markdown as fmt
from keyboards.inline.callbacks_data import names_callback, subjects_callback
from keyboards.inline.get_inline_keyboards import get_subjects_keyboard, get_names_keyboard
import re

logger = get_logger()


def call_errors_handler(func):
    async def wrapper(*args, **kwargs):
        call = args[0]
        try:
            await func(*args, *kwargs)
        except RetryAfter as ex:
            text = ex.args[0]
            seconds = re.search(r'\d{1,2}', text).group()
            await call.answer(f'Try again in {seconds} seconds', show_alert=True)
        except MessageNotModified:
            ...
        except Exception:
            logger.exception('An unexpected error occurred')

    return wrapper


def get_response(index, url):
    with requests.session() as session:
        session.post(POST_URL,
                     data={
                         'username': df['Login'][index],
                         'password': df['Password'][index],
                         'grant_type': 'password'
                     })
        session.get(AUTH_URL)
        response = session.get(url)
    return response


@call_errors_handler
async def _confirm_person(call, callback_data):
    index = int(callback_data.get('index'))
    surname = df['Full Name'][index].split()[0]
    response = get_response(index, SUBJECTS_URL)
    soup = BeautifulSoup(response.content, features='lxml')
    tags = [x.contents[1].contents[0] for x in soup.find_all('tr', {"data-year": data_year})]
    subjects = [x.text[:x.text.find(', Бакалавр')] for x in tags]
    if not subjects:
        text = f'Invalid login or password for {fmt.hbold(surname)}'
        subjects_links = []
    else:
        text = f'Choose the subject for {fmt.hbold(surname)}:'
        subjects_links = [x.get('href') for x in tags]
    reply_markup = get_subjects_keyboard(subjects, subjects_links, index)
    await call.message.edit_text(text=text,
                                 reply_markup=reply_markup)


@call_errors_handler
async def _choose_subject(call, callback_data):
    link = 'https://campus.kpi.ua' + PART_URL + callback_data.get('link')
    index = int(callback_data.get('index'))
    response = get_response(index, link)
    soup = BeautifulSoup(response.content, features='lxml')
    p_list = soup.find_all('p')
    total_mark = [x.text for x in p_list if 'Загальний результат:' in x.text][0]
    total_mark = re.search(r'\d{1,2}\.?\d{0,2}', total_mark).group()
    await call.answer(total_mark, show_alert=True)


@call_errors_handler
async def _return_to_person_choice(call):
    await call.message.edit_text(text='Choose the person:',
                                 reply_markup=get_names_keyboard())
