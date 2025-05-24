from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
from userbot_manager import start_login, submit_code, set_source, set_dest, toggle_forwarding

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

user_states = {}

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.reply("Welcome! Use /login to start Telegram login with your number.")

@dp.message_handler(commands=["login"])
async def login(msg: types.Message):
    user_id = msg.from_user.id
    user_states[user_id] = "awaiting_phone"
    await msg.reply("Send your phone number (with +91... format):")

@dp.message_handler(commands=["setsource"])
async def setsource(msg: types.Message):
    user_id = msg.from_user.id
    user_states[user_id] = "awaiting_source"
    await msg.reply("Send the source chat ID or username:")

@dp.message_handler(commands=["setdest"])
async def setdest(msg: types.Message):
    user_id = msg.from_user.id
    user_states[user_id] = "awaiting_dest"
    await msg.reply("Send the destination chat ID or username:")

@dp.message_handler(commands=["startforward"])
async def startfwd(msg: types.Message):
    await toggle_forwarding(msg.from_user.id, True)
    await msg.reply("Forwarding started.")

@dp.message_handler(commands=["stopforward"])
async def stopfwd(msg: types.Message):
    await toggle_forwarding(msg.from_user.id, False)
    await msg.reply("Forwarding stopped.")

@dp.message_handler()
async def handle_text(msg: types.Message):
    user_id = msg.from_user.id
    state = user_states.get(user_id)

    if state == "awaiting_phone":
        await start_login(user_id, msg.text, bot)
        user_states[user_id] = "awaiting_code"
        await msg.reply("OTP sent. Please enter the code:")

    elif state == "awaiting_code":
        result = await submit_code(user_id, msg.text)
        await msg.reply(result)
        user_states.pop(user_id, None)

    elif state == "awaiting_source":
        await set_source(user_id, msg.text)
        await msg.reply("Source chat set.")
        user_states.pop(user_id, None)

    elif state == "awaiting_dest":
        await set_dest(user_id, msg.text)
        await msg.reply("Destination chat set.")
        user_states.pop(user_id, None)

if __name__ == '__main__':
    executor.start_polling(dp)
