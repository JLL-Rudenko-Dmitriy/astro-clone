from pyrogram import Client, filters
from pyrogram.types import CallbackQuery


@Client.on_callback_query(filters.regex(r'^null$'))
async def null(bot: Client, callback_query: CallbackQuery):
    await callback_query.answer()