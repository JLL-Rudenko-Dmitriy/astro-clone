from typing import List, Dict, Any
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class YearsMenu:
    def __init__(
        self, 
        buttons: List[Dict[str, Any]], 
        items_in_page: int = 15,
        buttons_grid_x: int = 8,
    ):
        self.buttons = buttons
        self.buttons_grid_x = buttons_grid_x
        self.buttons_in_page = items_in_page


    def _create_menu(self, page: int = 1) -> Dict[str, Any]:
        start, end = (page - 1) * self.buttons_in_page, page * self.buttons_in_page
        pages = (len(self.buttons) + self.buttons_in_page - 1) // self.buttons_in_page
        
        keyboard = []
        for i in range(start, end, self.buttons_grid_x):
            row = [
                InlineKeyboardButton(
                    text=year,
                    callback_data=f'year {year}'
                )
                for year in self.buttons[i:i + self.buttons_grid_x]
            ]
            keyboard.append(row)

        enter_button = [
            InlineKeyboardButton(text='Ввести год', callback_data='.pmenu enter year')
        ]
        
        navigation_buttons = [
            InlineKeyboardButton(text=' ', callback_data='null') if page == 1 else InlineKeyboardButton('←', callback_data=f'.pmenu page {page-1}'),
            InlineKeyboardButton(text=' ', callback_data='null') if page == pages else InlineKeyboardButton('→', callback_data=f'.pmenu page {page+1}')
        ]

        return InlineKeyboardMarkup([*keyboard, navigation_buttons, enter_button])

    def get_total_pages(self) -> int:
        return (len(self.buttons) + self.buttons_in_page - 1) // self.buttons_in_page

    def get_page(self, page: int = 1) -> Dict[str, Any]:
        return self._create_menu(page)
    
if __name__ == '__main__':
    items = [
        'button1',
        'button2',
        'button3'
    ]

    menu = YearsMenu(items)
    page_menu = menu.get_page(1)

    print(page_menu['markup'].inline_keyboard)