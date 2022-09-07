
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from keyboards.default.markups import all_right_message, cancel_message, submit_markup
from aiogram.types import Message
from states import SosState
from filters import IsUser
from loader import dp, db


@dp.message_handler(commands='daftar_admin')
async def cmd_sos(message: Message):
    await SosState.question.set()
    await message.answer('<b>Silakan isi Biodata Dibawah:</b>\n\nNama :\nUmur :\nJenis Kelamanin :\nAsal Kota :\nPendidikan :\nTanggal.Bulan.Tahun Lahir :\nKesibukan :\nUsername Telegram :\n\n◻️ <b>Syarat Dan Ketentuan:</b>\n• Wanita Umur 19+\n• Tidak Boleh Penasaran\n• Tidak Boleh Terpaksa\n• Tidak Mudah Bosan\n• Berpengalaman\n\n◾ <b>Kelebihan:</b>\n• Bisa Mengambil Manfaat Dari Seseorang Curhat.\n\n◾ <b>Kekurangan:</b>\n• Unpaid', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=SosState.question)
async def process_question(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text

    await message.answer('Apakah Data Sudah Terisi Semua Dengan Benar?', reply_markup=submit_markup())
    await SosState.next()


@dp.message_handler(lambda message: message.text not in [cancel_message, all_right_message], state=SosState.submit)
async def process_price_invalid(message: Message):
    await message.answer('⛔ Tidak ada pilihan seperti itu')


@dp.message_handler(text=cancel_message, state=SosState.submit)
async def process_cancel(message: Message, state: FSMContext):
    await message.answer('Dibatalkan!', reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(text=all_right_message, state=SosState.submit)
async def process_submit(message: Message, state: FSMContext):

    cid = message.chat.id

    if db.fetchone('SELECT * FROM questions WHERE cid=?', (cid,)) == None:

        async with state.proxy() as data:
            db.query('INSERT INTO questions VALUES (?, ?)',
                     (cid, data['question']))

        await message.answer('Ok,Data Kamu Sedang Diproses!', reply_markup=ReplyKeyboardRemove())

    else:

        await message.answer('🙅 Kamu Hanya Bisa Daftar Sekali.', reply_markup=ReplyKeyboardRemove())

    await state.finish()
