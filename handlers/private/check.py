from pyrogram import Client
from pyrogram.types import Message

from misc.database import DataBase
from misc.utils import (
    get_keyboard,
    get_string,
    get_sender
)

db = DataBase()


async def check(bot: Client, message: Message):
    from_user = get_sender(message)
    user_id = from_user.id
    
    user_data = await db.get_user_data(user_id)
    gender = user_data.get('gender')
    day = user_data.get('day')
    month = user_data.get('month')
    year = user_data.get('year')
    hour = user_data.get('hour')
    minute = user_data.get('minute')
    city = user_data.get('city')
    
    format_hour = f'0{hour}' if len(str(hour)) == 1 else hour
    format_minute =  f'0{minute}' if len(str(minute)) == 1 else minute
    
    time = f'{format_hour}:{format_minute}' if hour and minute else '—'
    format_day = f'0{day}' if len(str(day)) == 1 else day
    format_month = f'0{month}' if len(str(month)) == 1 else month
    format_gender = 'Мужчина' if gender == 1 else 'Девушка'
    
    await bot.send_photo(
        chat_id=user_id,
        photo='./photos/3.jpg',
        caption=get_string('check').format(
            gender=format_gender,
            day=format_day,
            month=format_month,
            year=year,
            time=time,
            city=city
        ),
        reply_markup=get_keyboard('check')
    )
    
    await message.delete()
