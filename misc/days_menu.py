from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from calendar import monthrange
import datetime


months = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь'
}



def to_subscript(num):
    subscript_nums = "₀₁₂₃₄₅₆₇₈₉"
    return ''.join(subscript_nums[int(digit)] for digit in str(num))


def generate_inline_buttons(year, month, day: int = None):
    buttons = []

    buttons.append(
        [InlineKeyboardButton(
            text=f'{year} г.',
            callback_data='edit year'
        ),
        InlineKeyboardButton(
            text=months[month],
            callback_data='edit month'
        )]
    )
    
    # Добавляем дни недели
    days_of_week = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    buttons.append([
        InlineKeyboardButton(
            text=day_of_week,
            callback_data=' '
        )
        for day_of_week in days_of_week
    ])
    
    # Получаем первый день недели и количество дней в месяце
    first_day, num_days = monthrange(year, month)
    
    # Заполняем числами из предыдущего месяца
    previous_month_days = []
    if first_day != 0:
        previous_month_last_day = (datetime.date(year, month, 1) - datetime.timedelta(days=1)).day
        for i in range(first_day):
            previous_month = 12 if month-1 == 0 else month-1
            previous_month_day = previous_month_last_day - (first_day - 1 - i)
            previous_month_subscript_day = to_subscript(previous_month_day)
            
            previous_month_days.append(
                InlineKeyboardButton(
                    text=previous_month_subscript_day,
                    callback_data=f'month {previous_month}'
                )
            )
    
    # Заполняем числами текущего месяца
    current_month_days = [
        InlineKeyboardButton(
            text=f'✓{num_day}' if num_day == day else num_day,
            callback_data=f'day {num_day}'
        ) 
        for num_day in range(1, num_days + 1)
    ]
    
    # Заполняем числами из следующего месяца
    next_month_days = []
    while (len(previous_month_days) + len(current_month_days) + len(next_month_days)) % 7 != 0:
        next_month = 1 if month+1 == 13 else month+1
        next_month_day = len(next_month_days) + 1
        next_month_subscript_day = to_subscript(next_month_day)
        
        next_month_days.append(
            InlineKeyboardButton(
                text=next_month_subscript_day,
                callback_data=f'month {next_month}'
            )
        )
    
    
    # Формируем строки кнопок
    all_days = previous_month_days + current_month_days + next_month_days
    for i in range(0, len(all_days), 7):
        buttons.append(all_days[i:i+7])
    
    if day:
        format_month = f'0{month}' if len(str(month)) == 1 else month
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f'Выбрать {day}.{format_month}.{year} →',
                    callback_data='select'
                )
            ]
        )
    
    return InlineKeyboardMarkup(buttons)

# # Пример использования
# year = 2023
# month = 6
# buttons = generate_inline_buttons(year, month)
