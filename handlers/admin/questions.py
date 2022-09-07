
from handlers.user.menu import questions
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from keyboards.default.markups import all_right_message, cancel_message, submit_markup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.types.chat import ChatActions
from states import AnswerState
from loader import dp, db, bot
from filters import IsAdmin

question_cb = CallbackData('question', 'cid', 'action')


@dp.message_handler(IsAdmin(), text=questions)
async def process_questions(message: Message):

    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    questions = db.fetchall('SELECT * FROM questions')

    if len(questions) == 0:

        await message.answer('❗ Belum Ada Yang Mendaftar Menjadi Calon Admin.')

    else:

        for cid, question in questions:

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(
                '💁 Balas Pesan', callback_data=question_cb.new(cid=cid, action='answer')))

            await message.answer(question, reply_markup=markup)


@dp.callback_query_handler(IsAdmin(), question_cb.filter(action='answer'))
async def process_answer(query: CallbackQuery, callback_data: dict, state: FSMContext):

    async with state.proxy() as data:
        data['cid'] = callback_data['cid']

    await query.message.answer('Sekarang Tulis Jawaban Kamu?', reply_markup=ReplyKeyboardRemove())
    await AnswerState.answer.set()


@dp.message_handler(IsAdmin(), state=AnswerState.answer)
async def process_submit(message: Message, state: FSMContext):

    async with state.proxy() as data:
        data['answer'] = message.text

    await AnswerState.next()
    await message.answer('Memastikan, bahwa kamu tidak membuat kesalahan dalam menjawab!', reply_markup=submit_markup())


@dp.message_handler(IsAdmin(), text=cancel_message, state=AnswerState.submit)
async def process_send_answer(message: Message, state: FSMContext):
    await message.answer('Dibatalkan!', reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(IsAdmin(), text=all_right_message, state=AnswerState.submit)
async def process_send_answer(message: Message, state: FSMContext):

    async with state.proxy() as data:

        answer = data['answer']
        cid = data['cid']

        question = db.fetchone(
            'SELECT question FROM questions WHERE cid=?', (cid,))[0]
        db.query('DELETE FROM questions WHERE cid=?', (cid,))
        text = f'===========================\n<b>Data anda</b>\n===========================\n{question}\n===========================\n\n===========================\n<b>Hasil Persetujuan</b>\n===========================\n{answer}\n==========================='

        await message.answer('Terkirim!', reply_markup=ReplyKeyboardRemove())
        await bot.send_message(cid, text)

    await state.finish()
