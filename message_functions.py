from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
from loader import bot
from aiogram import types
from utils.logging import get_logger

logger = get_logger(handle_info=False)


async def delete_message(message: types.Message = None, message_id: int = 0, chat_id: int = 0):
    if message:
        msg_id = message.message_id
        chat_id = message.chat.id
    else:
        msg_id = message_id
        chat_id = chat_id
    try:
        await bot.delete_message(chat_id=chat_id, message_id=msg_id)
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        ...
    except Exception:
        logger.exception('An unexpected error occurred')
