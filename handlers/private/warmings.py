from pyrogram import Client, errors
from pyrogram.types import CallbackQuery

from pyrostep.shortcuts import inlinekeyboard

from misc.cyookassa import CYooKassa
from misc.database import DataBase
from misc.utils import (
    get_sender,
    get_string
)

from datetime import datetime
import asyncio, pytz


db = DataBase()
yk = CYooKassa()

async def warmings(bot: Client, callback_query: CallbackQuery):
    from_user = get_sender(callback_query)
    user_id = from_user.id
    
    user_data = await db.get_user_data(user_id)
    user_year = user_data.get('year')
    user_month = user_data.get('month')
    user_day = user_data.get('day')
    
    format_day = f'0{user_day}' if len(str(user_day)) == 1 else user_day
    format_month = f'0{user_month}' if len(str(user_month)) == 1 else user_month
    
    tz = pytz.timezone('Europe/Moscow')
    
    interval_seconds = 3 * 60 * 60
    
    while True:
        current_time = datetime.now(tz)
        current_hour = current_time.hour
        
        if current_hour >= 9:
            await asyncio.sleep(interval_seconds)
            
            user_data = await db.get_user_data(user_id)
            payment_id = user_data.get('payment_id')               
            payment_url = user_data.get('payment_url')               
            
            markup = inlinekeyboard([[['👉 Получить расшифровку', payment_url, 'url']]])
            
            if not await yk.payment_is_paid(payment_id):
                try:
                    await bot.send_photo(         
                        chat_id=user_id,
                        photo='./photos/5.jpg',
                        caption=get_string('warming_0'),
                        reply_markup=markup
                    )
                except errors.UserIsBlocked:
                    break
            else:    
                break
                
            await asyncio.sleep(interval_seconds)

            payment_id = await db.get_user_payment_id(user_id)
            
            if not await yk.payment_is_paid(payment_id):
                await bot.send_photo(
                    chat_id=user_id,
                    photo='./photos/6.jpg',
                    caption=get_string('warming_1'),
                    reply_markup=markup
                )
            else:
                break

            await asyncio.sleep(interval_seconds)

            payment_id = await db.get_user_payment_id(user_id)

            if not await yk.payment_is_paid(payment_id):
                await bot.send_photo(
                    chat_id=user_id,
                    photo='./photos/7.jpg',
                    caption=get_string('warming_2'),
                    reply_markup=markup
                )
            else:
                break

            await asyncio.sleep(interval_seconds)

            payment_id = await db.get_user_payment_id(user_id)

            if not await yk.payment_is_paid(payment_id):
                if user_day and user_month and user_year:
                    await bot.send_photo(
                        chat_id=user_id,
                        photo='./photos/8.jpg',
                        caption=get_string('warming_3').format(
                            day=format_day,
                            month=format_month,
                            year=user_year
                        ),
                        reply_markup=markup
                )
            else:
                break
