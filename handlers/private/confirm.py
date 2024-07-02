from pyrogram import Client, filters, enums
from pyrogram.types import CallbackQuery, Message

from pyrostep import wait_for

from misc.database import DataBase
from misc.utils import (
    get_keyboard,
    get_string,
    get_sender
)

import asyncio

db = DataBase()

@Client.on_callback_query(filters.regex(r'^confirm$'))
async def confirm(bot: Client, callback_query: CallbackQuery):
    from_user = get_sender(callback_query)
    user_id = from_user.id
    
    await callback_query.edit_message_reply_markup()
    await bot.send_message(
        chat_id=user_id,
        text=get_string('wait')
    )
    
    await bot.send_chat_action(user_id, enums.ChatAction.TYPING)
    await asyncio.sleep(5)
    
    await bot.send_message(
        chat_id=user_id,
        text=get_string('you_can_read'),
        reply_markup=get_keyboard('you_can_read')
    )
