from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message

from pyrostep import wait_for

from misc.days_menu import generate_inline_buttons
from misc.database import DataBase
from misc.utils import (
    get_keyboard,
    get_string,
    get_sender
)

db = DataBase()

@Client.on_callback_query(filters.regex(r'^select$'))
async def time(bot: Client, callback_query: CallbackQuery):
    from_user = get_sender(callback_query)
    user_id = from_user.id
    
    message = await bot.send_message(
        chat_id=user_id,
        text=get_string('time'),
        reply_markup=get_keyboard('time')
    )
    
    await callback_query.message.delete()
    
    answer: Message = await wait_for(user_id)
    value = answer.text
    
    try:
        if ':' in value:
            hour, minute = value.split(':')
            
            if len(str(hour)) == 2 and 0 < int(hour) <= 23:
                await db.update_user_hour(user_id, hour)
            else:
                await db.update_user_hour(user_id, None)
            
            if len(str(minute)) == 2 and 0 < int(minute) <= 59:
                await db.update_user_minute(user_id, minute)
            else:
                await db.update_user_minute(user_id, None)    
        else:
            await db.update_user_minute(user_id, None)
            await db.update_user_hour(user_id, None)
    except:
        await db.update_user_minute(user_id, None)
        await db.update_user_hour(user_id, None)
        
    from handlers.private.city import city
    await city(bot, message)