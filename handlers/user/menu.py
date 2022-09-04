
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove
from loader import dp
from filters import IsAdmin, IsUser
from aiogram import executor, types

from data import config

catalog = '🗣️ Info Penting'
balance = '📝 Rules Member'
cart = '📒 Statistik Bot'
delivery_status = '🍻 Donasi Kopi'

settings = '➕ Add Info Penting'
orders = '📄 Laporan Channel'
questions = '👥 Daftar Admin'
user_message = '✅ Aktifkan Menu Pengguna (🔐)'

@dp.message_handler(IsAdmin(), commands='menu')
async def admin_menu(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(settings)
    markup.add(questions, orders)
    markup.row(user_message)

    await message.answer('<b>•Menu Admin•</b>\n\n❗Menu ini Hanya Terlihat Oleh Admin BottyCu (Ganti Akun Untuk Melihat Menu Pengguna)\n\n🔐 <b>(EMOJI ini berarti tombol yang tidak boleh ditekan oleh siapa pun kecuali sendi)</b> (chat sendi kalau tidak sengaja tertekan)', reply_markup=markup)

@dp.message_handler(IsUser(), commands='menu')
async def user_menu(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(catalog)
    markup.add(balance, cart)
    markup.add(delivery_status)

    await message.answer('<b>•Menu Pengguna•</b>\n<b>Channel:</b>@BottyCu\n<b>Bot:</b>@CurhatBarengBottyBot\n\n• /hapus_tombol - <b>untuk menghapus tombol</b>', reply_markup=markup)

@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):

    cid = message.chat.id
    if cid in config.ADMINS:
        config.ADMINS.remove(cid)

    await message.answer('Mode pengguna diaktifkan.', reply_markup=ReplyKeyboardRemove())
