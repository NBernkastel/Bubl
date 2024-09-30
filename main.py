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


@app.post('/api/get_link', response_model=str)
async def get_link(data: LinkModel):
    prices = [LabeledPrice(label=f"{d['name']} X{d['qual']}", amount=d['amount'] * 100) for d in data.products]
    if len(prices) > 0:
        invoice_link = await bot.create_invoice_link(
            title='Билет на спектакль',
            description=f'Место',
            payload="hui",
            provider_token=secrets.KASSA_TOKEN,
            photo_url='https://wsyrqowenkpaazbnzxxk.supabase.co/storage/v1/object/sign/photo/cover.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJwaG90by9jb3Zlci5wbmciLCJpYXQiOjE3MjU4MTQ1ODQsImV4cCI6MTc1NzM1MDU4NH0.NdeHZ9hGr4vFi3WJFFp955wn26-qg7pHzMm13CK9pFU&t=2024-09-08T16%3A56%3A23.972Z',
            currency='rub',
            prices=prices,
            need_name=True,
            need_phone_number=True,
            request_timeout=60,
        )
        return invoice_link
    return HTTPException(detail="Wrong data", status_code=status.HTTP_400_BAD_REQUEST)
