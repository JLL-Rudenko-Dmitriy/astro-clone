from pyrogram import Client, filters
from pyrogram.types import Message

from misc.database import DataBase
from misc.utils import (
    get_keyboard,
    get_string,
    get_sender
)

db = DataBase()


@Client.on_message(filters.command(['start']) & filters.private)
async def start(bot: Client, message: Message):
    from_user = get_sender(message)
    user_id = from_user.id
    
    first_name = from_user.first_name
    username = from_user.username
    
    if not await db.user_exists(user_id):
        await db.add_user(
            user_id=user_id,
            first_name=first_name,
            username=username
        )
    
    await bot.send_photo(
        chat_id=user_id,
        photo='./photos/2.jpg',
        caption=get_string('start'),
        reply_markup=get_keyboard('start')
    )