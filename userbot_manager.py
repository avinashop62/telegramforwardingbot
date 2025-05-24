from telethon import TelegramClient, events
import os

sessions_dir = "sessions"
os.makedirs(sessions_dir, exist_ok=True)

user_clients = {}
chat_config = {}
forwarding_status = {}

async def start_login(user_id, phone, bot):
    client = TelegramClient(f"{sessions_dir}/{user_id}", api_id=20231234, api_hash="your_api_hash")
    await client.connect()
    sent = await client.send_code_request(phone)
    user_clients[user_id] = {"client": client, "phone": phone, "code_hash": sent.phone_code_hash}

async def submit_code(user_id, code):
    session = user_clients.get(user_id)
    if not session:
        return "Session not found. Use /login again."
    client = session["client"]
    try:
        await client.sign_in(session["phone"], code)
        await start_forwarding(user_id, client)
        return "Login successful."
    except Exception as e:
        return f"Login failed: {str(e)}"

async def set_source(user_id, source):
    chat_config.setdefault(user_id, {})["source"] = source

async def set_dest(user_id, dest):
    chat_config.setdefault(user_id, {})["dest"] = dest

async def start_forwarding(user_id, client):
    forwarding_status[user_id] = True

    @client.on(events.NewMessage)
    async def handler(event):
        if not forwarding_status.get(user_id):
            return
        config = chat_config.get(user_id, {})
        if str(event.chat_id) == str(config.get("source")):
            await client.send_message(config.get("dest"), event.message)

    await client.start()
    client.loop.create_task(client.run_until_disconnected())

async def toggle_forwarding(user_id, status):
    forwarding_status[user_id] = status

if __name__ == "__main__":
    import asyncio
    print("Userbot manager is active.")
    loop = asyncio.get_event_loop()
    loop.run_forever()  # Keeps the process alive for event handlers
