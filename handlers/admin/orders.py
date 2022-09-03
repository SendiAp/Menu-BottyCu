
from aiogram.types import Message
from loader import dp, db
from handlers.user.menu import orders
from filters import IsAdmin

@dp.message_handler(IsAdmin(), text=orders)
async def process_orders(message: Message):
    
    orders = db.fetchall('SELECT * FROM orders')
    
    if len(orders) == 0: await message.answer('<b>Gambaran</b>\n\n<b>204</b>+6(3.0%)\nPengikut\n\n<b>815</b>+607(291.8%)\nDilihat per postingan\n\n<b>24 Agu 2022 - 31 Agu 2022</b>\n\n<b>62.75%</b>\nNotifikasi Diaktifkan\n\n<b>35</b>\nDibagikan per postingan')
    else: await order_answer(message, orders)

async def order_answer(message, orders):

    res = ''

    for order in orders:
        res += f'Memesan <b>Tidak.{order[3]}</b>\n\n'

    await message.answer(res)
