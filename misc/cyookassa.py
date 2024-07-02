from aiohttp import ClientSession
from base64 import b64encode
from json import dumps
from uuid import uuid4

from config import (
    YOOKASSA_SECRETKEY,
    YOOKASSA_SHOPID
)

class CYooKassa:
    def __init__(self):
        self.shop_id = YOOKASSA_SHOPID
        self.secret_key = YOOKASSA_SECRETKEY
        self.base_url = "https://api.yookassa.ru/v3/payments"
        self.auth = b64encode(f"{self.shop_id}:{self.secret_key}".encode()).decode()
        
    async def create_payment(self, amount: float, return_url: str, description: str = 'Natalia map', currency: str = 'RUB') -> dict[str, str]:
        headers = {
            "Idempotence-Key": str(uuid4()),
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.auth}"
        }
        
        data = {
            "amount": {
                "value": amount,
                "currency": currency
            },
            "confirmation": {
                "type": "redirect",
                "return_url": return_url
            },
              "payment_method_data": {
                "type": "sbp"
            },
            "receipt": {
                "customer": {
                    "email": "astralmap@yandex.ru"
                },
                "items": [{ 
                        "description": description,
                        "quantity": 1,
                        "amount": {
                            "value": amount,
                            "currency": currency
                        },
                        "vat_code": 1,
                    }
                ]
            },
            "capture": True,
            "description": description
        }
        
        async with ClientSession() as session:
            async with session.post(self.base_url, headers=headers, data=dumps(data)) as response:
                data = await response.json()
                confirmation = data.get('confirmation')
                
                if confirmation:
                    return {
                        'id': data.get('id'),
                        'url': confirmation.get('confirmation_url')}
                
                return {}

    async def payment_is_paid(self, payment_id: str) -> bool:
        headers = {
            "Authorization": f"Basic {self.auth}"
        }
        
        async with ClientSession() as session:
            async with session.get(f'{self.base_url}/{payment_id}', headers=headers) as response:
                data = await response.json()
                paid = data.get('paid', False)
                
                return paid


async def main():
    yookassa = CYooKassa()
    payment = await yookassa.create_payment('23.00', 'https://t.me/username?start=payment', 'Заказ №72')
    print(payment) 
    print('\n---------------------------------------\n')
    input()
    is_paid = await yookassa.payment_is_paid(payment['id'])
    print(is_paid)

if __name__ == '__main__':
    import asyncio
    
    asyncio.run(main())
