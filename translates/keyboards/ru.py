from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(
            text='Девушка',
            callback_data='gender 2'
        )],
        [InlineKeyboardButton(
            text='Мужчина',
            callback_data='gender 1'
        )]
    ]
)

months = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(
            text="Январь", 
            callback_data="month 1"
        ), 
        InlineKeyboardButton(
            text="Февраль", 
            callback_data="month 2"
        ), 
        InlineKeyboardButton(
            text="Март", 
            callback_data="month 3"
        )],
        [InlineKeyboardButton(
            text="Апрель", 
            callback_data="month 4"
        ), 
        InlineKeyboardButton(
            text="Май", 
            callback_data="month 5"
        ), 
        InlineKeyboardButton(
            text="Июнь", 
            callback_data="month 6"
        )],
        [InlineKeyboardButton(
            text="Июль", 
            callback_data="month 7"
        ), 
        InlineKeyboardButton(
            text="Август", 
            callback_data="month 8"
        ), 
        InlineKeyboardButton(
            text="Сентябрь", 
            callback_data="month 9"
        )],
        [InlineKeyboardButton(
            text="Октябрь", 
            callback_data="month 10"
        ), 
        InlineKeyboardButton(
            text="Ноябрь", 
            callback_data="month 11"
        ), 
        InlineKeyboardButton(
            text="Декабрь", 
            callback_data="month 12"
        )],
        [InlineKeyboardButton(
            text="← Назад",
            callback_data='back'
        )]

    ]
)

time = ReplyKeyboardMarkup(
    [
        [KeyboardButton(
            text='Не помню'
        )],
    ],
    resize_keyboard=True
)

cancel = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(
            text='× Отменить',
            callback_data='cancel'
        )]
    ]
)

check = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(
            text='Подтвердить ✅',
            callback_data='confirm'
        )]
    ]
)

you_can_read = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(
            text='Да',
            callback_data='can read 1'
        )],
        [InlineKeyboardButton(
            text='Нет',
            callback_data='can read 0'
        )]
    ]
)
