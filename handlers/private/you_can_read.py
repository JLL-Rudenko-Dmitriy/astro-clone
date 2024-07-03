from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InputMediaPhoto

from pyrostep.shortcuts import inlinekeyboard

from misc.cyookassa import CYooKassa
from misc.database import DataBase
from misc.utils import (
    get_day_and_month,
    get_string,
    get_sender
)

import asyncio

db = DataBase()
yk = CYooKassa()


@Client.on_callback_query(filters.regex(r'^can read (.+)$'))
async def confirm(bot: Client, callback_query: CallbackQuery):
    from_user = get_sender(callback_query)
    user_id = from_user.id
    
    payment = await yk.create_payment(599, f'https://t.me/{(await bot.get_me()).username}')
    
    payment_id = payment.get('id')
    payment_url = payment.get('url')

    await db.update_user_payment_id(user_id, payment_id)
    await db.update_user_payment_url(user_id, payment_url)

    await bot.send_media_group(
        chat_id=user_id,
        media=[
            InputMediaPhoto('./photos/examples/1.jpg'),
            InputMediaPhoto('./photos/examples/2.jpg'),
            InputMediaPhoto('./photos/examples/3.jpg'),
            InputMediaPhoto('./photos/examples/4.jpg', caption='пример натальной карты, которую вы получите')
        ],
    )
    
    await bot.send_photo(
        chat_id=user_id,
        photo='./photos/4.jpg',
        caption=get_string('ready'),
        reply_markup=inlinekeyboard([[['👉 Получить расшифровку', payment_url, 'url']]])
    )
    
    await callback_query.message.delete()
    
    from handlers.private.warmings import warmings
    asyncio.create_task(warmings(bot, callback_query))
    