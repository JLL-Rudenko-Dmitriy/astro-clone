from pyrogram import Client, filters, errors
from pyrogram.types import Message


from misc.database import DataBase
from misc.utils import get_sender

from config import ADMIN_IDS


db = DataBase()


async def is_admin(_, bot: Client, message: Message):
    from_user = get_sender(message)
    user_id = from_user.id

    if user_id in ADMIN_IDS:
        return True
    else:
        return False


admin = filters.create(is_admin)
"""CFilter user is admin."""
