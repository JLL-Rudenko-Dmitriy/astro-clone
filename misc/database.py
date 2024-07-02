from typing import List, Dict, Any
from ast import literal_eval

from aiosqlite import Connection, Cursor
import aiosqlite


class DataBase:
    def __init__(self) -> None:
        self.db_file = './data/database.db'

    async def _execute_query(self, query, *args) -> None:
        async with aiosqlite.connect(self.db_file) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)
                await conn.commit()

    async def _fetch_query(self, query, *args) -> Any:
        async with aiosqlite.connect(self.db_file) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)
                
                return await cursor.fetchall()
            
    async def _cursor_query(self, query: str = None, *args) -> tuple[Connection, Cursor]:
        conn = await aiosqlite.connect(self.db_file)
        cursor = await conn.cursor()
        if query:
            await cursor.execute(query, args)
        
        return conn, cursor
                

    async def get_user_ids(self) -> List[int]:
        fetches = await self._fetch_query("SELECT `user_id` FROM `users`")

        return [fetch[0] for fetch in fetches] if fetches else []
    
    async def user_exists(self, user_id: int) -> bool:
        user_id = user_id if isinstance(user_id, int) else int(user_id) if user_id.isdigit() else None  
        user_ids = await self.get_user_ids()
        
        return True if user_id in user_ids else False

    async def add_user(self, user_id: int, first_name: str, username: str) -> None:
        await self._execute_query("INSERT INTO `users` (`user_id`, `first_name`, `username`) VALUES (?, ?, ?)", user_id, first_name, username)

    async def get_user_data(self, user_id: int) -> Dict[str, Any]:
        fetch = await self._fetch_query("SELECT * FROM `users` WHERE `user_id` = ?", user_id)
        columns = await self._fetch_query("PRAGMA table_info(users)")
        column_names = [column[1] for column in columns]
        
        return dict(zip(column_names, fetch[0]))
    
    async def update_user_gender(self, user_id: int, gender: int) -> None:
        await self._execute_query("UPDATE `users` SET `gender` = ? WHERE `user_id` = ?", gender, user_id)

    async def update_user_year(self, user_id: int, year: int) -> None:
        await self._execute_query("UPDATE `users` SET `year` = ? WHERE `user_id` = ?", year, user_id)

    async def update_user_month(self, user_id: int, month: int) -> None:
        await self._execute_query("UPDATE `users` SET `month` = ? WHERE `user_id` = ?", month, user_id)
    
    async def update_user_day(self, user_id: int, day: int) -> None:
        await self._execute_query("UPDATE `users` SET `day` = ? WHERE `user_id` = ?", day, user_id)
    
    async def update_user_hour(self, user_id: int, hour: int) -> None:
        await self._execute_query("UPDATE `users` SET `hour` = ? WHERE `user_id` = ?", hour, user_id)
        
    async def update_user_minute(self, user_id: int, minute: int) -> None:
        await self._execute_query("UPDATE `users` SET `minute` = ? WHERE `user_id` = ?", minute, user_id)
        
    async def update_user_city(self, user_id: int, city: str) -> None:
        await self._execute_query("UPDATE `users` SET `city` = ? WHERE `user_id` = ?", city, user_id)
    
    async def update_user_payment_id(self, user_id: int, payment_id: str) -> None:
        await self._execute_query("UPDATE `users` SET `payment_id` = ? WHERE `user_id` = ?", payment_id, user_id)
    
    async def update_user_payment_url(self, user_id: int, payment_url: str) -> None:
        await self._execute_query("UPDATE `users` SET `payment_url` = ? WHERE `user_id` = ?", payment_url, user_id)

    async def get_user_payment_id(self, user_id: int) -> str:
        fetch = await self._fetch_query("SELECT `payment_id` FROM `users` WHERE `user_id` = ?", user_id)

        return fetch[0][0] if fetch else None
        
    async def get_payments(self) -> list[str]:
        fetches = await self._fetch_query("SELECT `user_id`, `payment_id` FROM `users` WHERE `payment_id` IS NOT NULL")
        
        return [fetch for fetch in fetches] if fetches else []
        
if __name__ == '__main__':
    import asyncio
    
    db = DataBase()
    b = asyncio.run(db.get_user_payment_id(1563296065))
    print(b)
