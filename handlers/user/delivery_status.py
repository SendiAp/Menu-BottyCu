
from aiogram.types import Message
from loader import dp, db
from .menu import delivery_status
from filters import IsUser

@dp.message_handler(IsUser(), text=delivery_status)
async def process_delivery_status(message: Message):
    
    orders = db.fetchall('SELECT * FROM orders WHERE cid=?', (message.chat.id,))
    
    if len(orders) == 0: await message.answer('Wow... sepertinya kamu rajin pakai bot botty, yuk donasi untuk pengembangan bot botty, caranya bisa dengan bayar via <b>Dana (085894831504)</b> atau bila ingin menggunakan metode pembayaran lainnya bisa hubungi telegram @pikyus1 atau bisa juga dengan kirim email ke <b>snktlg4@gmail.com</b> Semua donasi yang masuk akan digunakan untuk penyewaan server. terima kasih :).')
    else: await delivery_status_answer(message, orders)

async def delivery_status_answer(message, orders):

    res = ''

    for order in orders:

        res += f'Memesan <b>Tidak.{order[3]}</b>'
        answer = [
            ' ada dalam stok.',
            ' aku di jalan!',
            ' telah tiba dan menunggumu di kantor pos!'
        ]

        res += answer[0]
        res += '\n\n'

    await message.answer(res)
