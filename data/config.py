from environs import Env
import pandas as pd

env = Env()
env.read_env()
BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
CHAT = env.int("CHAT")
TEST_CHAT = env.int("TEST_CHAT")
FILE = env.str("FILE")
df = pd.read_csv(FILE)
URL = 'https://ecampus.kpi.ua/'
data_year = '2021-2022'
PART_LINK = 'https://campus.kpi.ua/student/index.php?mode=studysheet'
