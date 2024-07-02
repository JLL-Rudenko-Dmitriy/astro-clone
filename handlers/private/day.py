from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message

from misc.days_menu import generate_inline_buttons
from misc.database import DataBase
from misc.utils import (
    get_keyboard,
    get_string,
    get_sender
)

db = DataBase()

@Client.on_callback_query(filters.regex(r'^month (.+)$'))
async def day(bot: Client, callback_query: CallbackQuery):
    from_user = get_sender(callback_query)
    user_id = from_user.id
    month = callback_query.matches[0].groups()[0]
    
    await db.update_user_month(user_id, month)
    
    user_data = await db.get_user_data(user_id)
    year = user_data.get('year')
    
    markup = generate_inline_buttons(year, int(month))
    
    await callback_query.edit_message_reply_markup(
        reply_markup=markup
    )

@Client.on_callback_query(filters.regex(r'^edit (.+)$'))
async def edit(bot: Client, callback_query: CallbackQuery):
    edited = callback_query.matches[0].groups()[0]
    
    if edited == 'year':
        from handlers.private.birthdate import birthdate_wrapper
        await birthdate_wrapper(bot, callback_query)
    elif edited == 'month':
        from handlers.private.month import month_wrapper
        await month_wrapper(bot, callback_query)
        

@Client.on_callback_query(filters.regex(r'^day (.+)$'))
async def select_day(bot: Client, callback_query: CallbackQuery):
    from_user = get_sender(callback_query)
    user_id = from_user.id
    day = callback_query.matches[0].groups()[0]
    
    await db.update_user_day(user_id, day)
    
    user_data = await db.get_user_data(user_id)
    month = user_data.get('month')
    year = user_data.get('year')
    
    markup = generate_inline_buttons(int(year), int(month), int(day))
    
    await callback_query.edit_message_reply_markup(markup)