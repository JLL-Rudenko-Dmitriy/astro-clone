from pyrogram import Client, idle
from pyrogram.types import InputMediaPhoto
from pyrostep import listen

from pyrostep.shortcuts import inlinekeyboard

from misc.cyookassa import CYooKassa
from misc.astrology import Astrology
from misc.database import DataBase
from misc.logger import SimpleLogger, log
from misc.utils import get_coordinates

from config import (
    BOT_TOKEN,
    API_HASH,
    API_ID,
    DEBUG,
)

import asyncio

bot = Client('bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, plugins=dict(root='handlers'), workdir='./data')
listen(bot)

db = DataBase()
yk = CYooKassa()
al = Astrology()

async def payment_checker(bot: Client):
    while True:
        payments = await db.get_payments()
        for user_id, payment_id in payments:
            if await yk.payment_is_paid(payment_id):
                await db.update_user_payment_id(user_id, None)
                await db.update_user_payment_url(user_id, None)
                
                user_data = await db.get_user_data(user_id)
                user_year = user_data.get('year')
                user_month = user_data.get('month')
                user_day = user_data.get('day')
                user_hour = user_data.get('hour')
                user_minute = user_data.get('minute')
                city = user_data.get('city')
                
                year = user_year if user_year else 2000
                month = user_month if user_month else 1
                day = user_day if user_day else 1
                hour = user_hour if user_hour else 0 
                minute = user_minute if user_minute else 0

                latitude, longitude = get_coordinates(city)
                timezone = 5.5
                language = 'ru'
                
                url = al.get_pdf_url(day, month, year, hour, minute, latitude, longitude, timezone, language)
                await bot.send_message(user_id, f"Вот ваша натальная карта - {url}")

        await asyncio.sleep(10)


async def main():
    await bot.start()
    print(f'Bot Was Started in @{(await bot.get_me()).username}. ')
    log.info('Bot Was Started.')
    
    
    await asyncio.create_task(payment_checker(bot))
    await idle()

    print('Bot Was Stoped.')
    log.info('Bot Was Stoped.')
    
    await bot.stop()



if __name__ == '__main__':
    if DEBUG: SimpleLogger()
    bot.run(main())

