from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message

from misc.database import DataBase
from misc.utils import (
    get_keyboard,
    get_string,
    get_sender
)

db = DataBase()


@Client.on_callback_query(filters.regex(r'^year (.+)$'))
async def months(bot: Client, callback_query: CallbackQuery):
    from_user = get_sender(callback_query)
    user_id = from_user.id
    year = callback_query.matches[0].groups()[0]
    
    await db.update_user_year(user_id, year)
    await month_wrapper(bot, callback_query)
    
async def month_wrapper(bot: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_reply_markup(
        reply_markup=get_keyboard('months')
    )


@Client.on_callback_query(filters.regex(r'back'))
async def back(bot: Client, callback_query: CallbackQuery):
    from handlers.private.birthdate import birthdate_wrapper
    await birthdate_wrapper(bot, callback_query)