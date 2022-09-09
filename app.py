from aiogram import executor
from loader import dp
import handlers
from utils.set_bot_commands import set_default_commands
from utils.logging import get_logger

logger = get_logger(errors_to_file=True)


async def on_startup(dispatcher):
    try:
        await set_default_commands(dispatcher)
    except Exception:
        logger.exception('An unexpected error occurred')


if __name__ == '__main__':
    try:
        executor.start_polling(dispatcher=dp, on_startup=on_startup, skip_updates=True,
                               timeout=0.1)
    except TimeoutError as ex:
        logger.exception(ex)
    except Exception:
        logger.exception('An unexpected error occurred')
