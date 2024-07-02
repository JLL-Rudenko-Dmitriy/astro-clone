from pyrogram import Client
from pyrogram.types import Message

from pyrostep import wait_for

from misc.database import DataBase
from misc.utils import (
    get_keyboard,
    get_string,
    get_sender
)

db = DataBase()


async def city(bot: Client, message: Message):
    from_user = get_sender(message)
    user_id = from_user.id
    
    await bot.send_message(
        chat_id=user_id,
        text=get_string('city')
    )
    
    await message.delete()
    
    answer: Message = await wait_for(user_id)
    value = answer.text
    
    await db.update_user_city(user_id, value)
    
    from handlers.private.check import check
    await check(bot, message)