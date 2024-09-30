from aiogram.client.default import DefaultBotProperties
from aiogram.types import LabeledPrice
from fastapi import HTTPException, status
from fastapi import FastAPI
from aiogram import Bot

from config.instance import secrets
from database_config import supabase
from schemas import LinkModel

app = FastAPI()
default = DefaultBotProperties(parse_mode='Markdown', protect_content=False)
bot = Bot(token=secrets.TOKEN, default=default)


@app.get('/api/products/all')
def get_all_products():
    res = supabase.table('ProductData').select().execute().data
    return res


@app.get('/api/products/categories')
def get_by_category():
    res = supabase.table('Category').select().execute().data
    return res


@app.post('/api/get_link')
async def get_link(data: LinkModel):
    prices = [LabeledPrice(label=f"{d['name']} X{d['qual']}", amount=d['amount'] * 100) for d in data.products]
    if len(prices) > 0:
        invoice_link = await bot.create_invoice_link(
            title='Билет на спектакль',
            description=f'Место',
            payload="hui",
            provider_token=secrets.KASSA_TOKEN,
            currency='rub',
            prices=prices,
            need_name=True,
            need_phone_number=True,
            request_timeout=60,
        )
        return {"link":invoice_link}
    return HTTPException(detail="Wrong data", status_code=status.HTTP_400_BAD_REQUEST)
