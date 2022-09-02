
from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from filters import IsUser
from .menu import balance

# test card ==> 1111 1111 1111 1026, 12/22, CVC 000

# shopId 506751

# shopArticleId 538350


@dp.message_handler(IsUser(), text=balance)
async def process_balance(message: Message, state: FSMContext):
    await message.answer('Kami <b>Melarang Keras</b> Beberapa Aturan Yang Kami Buat , Ada Beberapa Aturan Yang Kami Buat , Kalian Harus Mengikuti Peraturan Ketika <b>Curhat DiBotty,</b> Team Sudah Membuat Peraturan <b>Yaitu:</b>\n\n• <b>Dilarang Keras Melakukan Spamner Menggunakan Kata Kata (P) Dll.</b>\n• <b>Dilarang Keras Untuk Mengirimkan Hal Pornografi</b>\n• <b>Dilarang Keras Berkata Kasar Ketika Sedang Obrolan Berlangsung.</b>\n\nSanksi Yang Diberikan Adalah : 📵 <b>Banned</b> (Tidak Bisa Mengirim Pesan Dalam Bot)')

