import re
import time
from aiogram.types import Message, CallbackQuery
from selenium.webdriver.common.by import By
from data.config import URL, df, data_year, PART_LINK
from keyboards.inline.callbacks_data import names_callback, subjects_callback
from keyboards.inline.get_inline_keyboards import get_names_keyboard, get_subjects_keyboard
from loader import dp
from selenium import webdriver
import aiogram.utils.markdown as fmt
import undetected_chromedriver as uc
from message_functions import delete_message
from utils.logging import get_logger


logger = get_logger()


def get_driver():
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    driver = uc.Chrome(options=options, use_subprocess=True)
    driver.get(URL)


@dp.message_handler(commands='get_marks')
async def choose_person(message: Message):
    await message.reply('Choose the person:', reply_markup=get_names_keyboard())
    await delete_message(message)


@dp.callback_query_handler(names_callback.filter(action='show'))
async def confirm_person(call: CallbackQuery, callback_data: dict):
    try:
        get_driver()
        index = int(callback_data.get('index'))
        surname = df['Full Name'][index].split()[0]
        driver.find_element(By.XPATH, "//input[@type='text']").send_keys(df['Login'][index])
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(df['Password'][index])
        driver.find_element(By.XPATH, "//input[@type='submit']").click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//button[normalize-space()="До поточної версії кампусу"]').click()
        time.sleep(1)
        driver.get('https://campus.kpi.ua/student/index.php?mode=studysheet')
        time.sleep(1)
        subjects_list = driver.find_elements(By.XPATH, f'//tr[@data-year="{data_year}"]')
        subjects = [x.text[:x.text.find(', Бакалавр')] for x in subjects_list]
        subjects_links = [x.find_element(By.TAG_NAME, 'a').get_attribute('href') for x in subjects_list]
        await call.message.edit_text(fmt.text(f'Choose the subject for {fmt.hbold(surname)}:'))
        await call.message.edit_reply_markup(get_subjects_keyboard(subjects, subjects_links))
    except Exception:
        logger.exception('An unexpected error occurred')
        await delete_message(call.message)
        driver.quit()


@dp.callback_query_handler(names_callback.filter(action='close'))
async def close_menu(call: CallbackQuery):
    await delete_message(call.message)
    driver.quit()


@dp.callback_query_handler(subjects_callback.filter(action='show'))
async def choose_subject(call: CallbackQuery, callback_data: dict):
    try:
        link = PART_LINK + callback_data.get('link')
        driver.get(link)
        time.sleep(1)
        total_mark_str = driver.find_element(By.XPATH, '//p[text()="Загальний результат: "]').text
        total_mark = re.search(r'\d{1,2}\.?\d{0,2}', total_mark_str).group()
        await call.answer(total_mark, show_alert=True)
    except Exception:
        logger.exception('An unexpected error occurred')
        await delete_message(call.message)
        driver.quit()


@dp.callback_query_handler(subjects_callback.filter(action='return'))
async def return_to_person_choice(call: CallbackQuery):
    try:
        driver.quit()
        await call.message.edit_text('Choose the person:')
        await call.message.edit_reply_markup(get_names_keyboard())
    except Exception:
        logger.exception('An unexpected error occurred')
        await delete_message(call.message)
        driver.quit()
