import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from keyboards.all_keyboards import main_kb, create_spec_kb, create_rat
from keyboards.inline_kbs import ease_link_kb, get_inline_kb, create_qst_inline_kb
from utils.my_utils import get_random_person
from create_bot import questions, bot

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    command_args = command.args
    if command_args:
        await message.answer(
            f'Запуск сообщения по команде /start используя фильтр CommandStart() с меткой <b>{command_args}</b>',
            reply_markup=main_kb(message.from_user.id))
    else:
        await message.answer(
            f'Запуск сообщения по команде /start используя фильтр CommandStart() без метки',
            reply_markup=main_kb(message.from_user.id))
        

@start_router.message(Command('start_2'))
async def cmd_start_2(message: Message):
    await message.answer(
        'Запуск сообщения по команде /start_2 используя фильтр Command()',
        reply_markup=create_spec_kb()
    )

@start_router.message(F.text == '/start_3')
async def cmd_start_3(message: Message):
    await message.answer(
        'Запуск сообщения по команде /start_3 используя магический фильтр F.text!',
        reply_markup=create_rat())
    

@start_router.message(F.text == 'Давай инлайн!')
async def get_inline_btn_link(message: Message):
    await message.answer('Вот тебе инлайн клавиатура со ссылками!', reply_markup=get_inline_kb())


@start_router.callback_query(F.data == 'get_person')
async def send_random_person(call: CallbackQuery):
    # await call.answer('Генерирую случайного пользователя')
    user = get_random_person()
    formatted_message = (
        f"👤 <b>Имя:</b> {user['name']}\n"
        f"🏠 <b>Адрес:</b> {user['address']}\n"
        f"📧 <b>Email:</b> {user['email']}\n"
        f"📞 <b>Телефон:</b> {user['phone_number']}\n"
        f"🎂 <b>Дата рождения:</b> {user['birth_date']}\n"
        f"🏢 <b>Компания:</b> {user['company']}\n"
        f"💼 <b>Должность:</b> {user['job']}\n"
    )
    await call.message.answer(formatted_message)
    await call.answer("Генерирую случайного пользователя", show_alert=False)


@start_router.callback_query(F.data == 'back_home')
async def back_home(call: CallbackQuery):
    await call.message.answer(
        f'Вы вернулись на главную клавиатуру',
        reply_markup=main_kb(call.from_user.id)
    )
    await call.answer("Вы вернулись на главную клавиатуру", show_alert=False)


@start_router.callback_query(F.data.startswith('qst_'))
async def get_answer(call: CallbackQuery):
    await call.answer()
    qst_id = int(call.data.replace('qst_', ''))
    qst_answer = questions[qst_id]
    msg_text = f'Ответ на вопрос {qst_answer.get("qst")}\n\n' \
               f'<b>{qst_answer.get("answer")}</b>\n\n' \
               f'Выбери другой вопрос:'
    async with ChatActionSender(bot=bot, chat_id=call.from_user.id, action="typing"):
        await asyncio.sleep(2)
        await call.message.answer(msg_text, reply_markup=create_qst_inline_kb(questions))


@start_router.message(Command('faq'))
async def faq_handler(message: Message):
    await message.answer(
        'Сообщение с инлайн клавиатурой с вопросами', 
        reply_markup=create_qst_inline_kb(questions)
    )