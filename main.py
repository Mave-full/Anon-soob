import asyncio
import logging
import config as cfg
import buttons as bt
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    CallbackQuery
)

router = Router()


class Form(StatesGroup):
    text = State()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}, что бы отправить анонимное сообщение напиши /anon или же нажми на кнопку ниже 👇.", reply_markup=bt.anon_kb())

@router.message(Command("anon"))
async def command_anon_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.text)
    await message.answer("Напишите сообщение что бы отправить его администраторам канала MAVER.", reply_markup=bt.canc_kb())

@router.callback_query(F.data == 'anon')
async def anon_callback(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.text)
    await call.message.answer("Напишите сообщение что бы отправить его администраторам канала MAVER.", reply_markup=bt.canc_kb())

@router.message(Form.text)
async def process_text(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.clear()
    await message.answer("Сообщение отправленно, вы возвращенны в меню \nнапиши /anon или же нажми на кнопку ниже 👇.", reply_markup=bt.anon_kb())
    for id in cfg.admins:
        await bot.send_message(id, text=f"У вас новое анонимное сообщение!\n\n<pre>{message.text}</pre>\n\nНе забудьте ответить на него!")

async def main() -> None:
    bot = Bot(cfg.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
