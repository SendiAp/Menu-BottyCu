
import os
import handlers
from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import config
from loader import dp, db, bot
import filters
import logging

filters.setup(dp)

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 5000))
user_message = 'Yakin , 100% Yakin'
admin_message = '✅ Aktifkan Menu Admin'

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(user_message)

    await message.answer('''Hai Sahabat! 👋
🤖 Saya asisten dari bot curhat botty, saya akan membantu menampilkan informasi dll.
    
📄 Untuk mempilkan semua menu atau informasi Kalian bisa klik /menu

👥 Kamu mau jadi bagian team Botty? daftarkan diri kamu menjadi admin Bottycu klik /daftar_admin

❓ Kamu wajib join channel Botty [@BottyCu] agar mendapatkan informasi terkini dari kami.

🤝 Ingin membuat iklan DiBot BottyCu? Hubungi pengembang <a href="https://t.me/pikyus1">Mas S</a>, dia tidak menggigit''',)

@dp.message_handler(commands='hapus_tombol')
async def cmd_tombol(message: types.Message):

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(user_message)

    await message.answer('''Apa Kamu Yakin Ingin Menghapus Tombolnya?''', reply_markup=markup)

@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):
    await message.answer('Ok, Saya Akan Menghapusnya.', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(commands='085894831504')
async def cmd_tombol(message: types.Message):

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(admin_message)

    await message.answer('''❗ <b>Peringatan</b>\n\n◾<b>Perintah ini hanya digunakan oleh admin Bottycu</b> aja jika admin Botty menyebarkan Perintah ini akan dikenakan sanksi berat.''', reply_markup=markup)

@dp.message_handler(text=admin_message)
async def admin_peringatan(message: types.Message):

    cid = message.chat.id
    if cid not in config.ADMINS:
        config.ADMINS.append(cid)

    await message.answer('✅ Menu Admin Berhasil Diaktifkan.\n\n◾ Silahkan Ketik /menu untuk memunculkan Tombol.', reply_markup=ReplyKeyboardRemove())

async def on_startup(dp):
    logging.basicConfig(level=logging.INFO)
    db.create_tables()

    await bot.delete_webhook()
    await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown():
    logging.warning("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot down")


if __name__ == '__main__':

    if "HEROKU" in list(os.environ.keys()):

        executor.start_webhook(
            dispatcher=dp,
            webhook_path=config.WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )

    else:

        executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
