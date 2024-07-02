from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message

from pyrostep import wait_for, unregister_steps

from misc.years_menu import YearsMenu
from misc.database import DataBase
from misc.utils import (
    get_keyboard,
    get_string,
    get_sender
)

import asyncio

db = DataBase()
ym = YearsMenu(range(1960, 2005), buttons_grid_x=3)

@Client.on_callback_query(filters.regex(r'^gender (.+)$'))
async def birthdate(bot: Client, callback_query: CallbackQuery):
    from_user = get_sender(callback_query)
    user_id = from_user.id
    gender = callback_query.matches[0].groups()[0]
    
    await db.update_user_gender(user_id, gender)
    await birthdate_wrapper(bot, callback_query)
    

async def birthdate_wrapper(bot: Client, callback_query: CallbackQuery):
    max_page = ym.get_total_pages()
    markup = ym.get_page(max_page)
    
    await callback_query.edit_message_text(
        text=get_string('birthdate'),
        reply_markup=markup
    )

@Client.on_callback_query(filters.regex(r'^.pmenu page (.+)$'))
async def pmenu_page(bot: Client, callback_query: CallbackQuery):
    page = callback_query.matches[0].groups()[0]
    markup = ym.get_page(int(page))
    
    await callback_query.edit_message_reply_markup(markup)

async def enter_error(bot: Client, callback_query: CallbackQuery):
    from_user = get_sender(callback_query)
    user_id = from_user.id
    
    temp_msg = await bot.send_message(
        chat_id=user_id,
        text='Нельзя выбрать указанный год!'
    )

    await asyncio.sleep(10)
    await temp_msg.delete()

@Client.on_callback_query(filters.regex(r'^.pmenu enter year$'))
async def pmenu_enter_year(bot: Client, callback_query: CallbackQuery):
    from_user = get_sender(callback_query)
    user_id = from_user.id
    
    await callback_query.answer()
    
    message = await bot.send_message(
        chat_id=user_id,
        text='Отправьте год...',
        reply_markup=get_keyboard('cancel')
    ) 
    
    while True:
        try:
            answer: Message = await wait_for(user_id)
        except Exception as e:
            return e
        else:
            await answer.delete()
            text = str(answer.text)
            value = int(text) if text.isdigit() else None
            
            if value:
                if 1960 <= value <= 2005:
                    await message.delete()
                    await db.update_user_year(user_id, value)
                    await callback_query.edit_message_reply_markup(get_keyboard('months'))
                else:
                    asyncio.create_task(enter_error(bot, callback_query))
            else:
                asyncio.create_task(enter_error(bot, callback_query))


@Client.on_callback_query(filters.regex(r'^cancel$'))
async def cancel(bot: Client, callback_query: CallbackQuery):
    from_user = get_sender(callback_query)
    user_id = from_user.id
    
    await unregister_steps(user_id)
    await callback_query.message.delete()