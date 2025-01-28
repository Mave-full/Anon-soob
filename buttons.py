from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

def anon_kb():
    anon_kb_list = [
        [InlineKeyboardButton(text="Анонимное сообщение", callback_data='anon')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=anon_kb_list)

def canc_kb():
    canc_kb_list = [
        [InlineKeyboardButton(text="Отмена", callback_data='cancel')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=canc_kb_list)