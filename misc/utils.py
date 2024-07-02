from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from geopy.geocoders import Nominatim

from datetime import datetime

import random

def get_sender(MessageOrCallbackQuery: Message | CallbackQuery):
    try:
        if MessageOrCallbackQuery.from_user.is_bot:
            try:
                return MessageOrCallbackQuery.message.chat.from_user
            except AttributeError:
                return MessageOrCallbackQuery.chat
        else:
            return MessageOrCallbackQuery.from_user
    except AttributeError:
        return MessageOrCallbackQuery.chat


def get_string(string: str, lang: str = 'ru') -> str:
    from translates.strings import ru
    
    longuages = {
        'ru': ru
    }
    
    return getattr(longuages[lang], string).strip()

def get_keyboard(keyboard: str, lang: str = 'ru') -> ReplyKeyboardMarkup | InlineKeyboardMarkup | str:
    from translates.keyboards import ru

    longuages = {
        'ru': ru
    }
    
    return getattr(longuages[lang], keyboard)


def get_day_and_month() -> tuple:
    months = {
        1: 'Января',
        2: 'Февраля',
        3: 'Марта',
        4: 'Апреля',
        5: 'Мая',
        6: 'Июня',
        7: 'Июля',
        8: 'Августа',
        9: 'Сентября',
        10: 'Октября',
        11: 'Ноября',
        12: 'Декабря'
    }
    

    today = datetime.today()
    day = today.day
    month = today.month
    
    return day, months[month]


def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="geo_locator")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        return random.uniform(-90, 90), random.uniform(-180, 180)