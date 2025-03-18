import os
from telethon.sessions import StringSession
from telethon import TelegramClient

# Load environment variables
TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID", 0))
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH", "")
TELEGRAM_SESSION_FILE = "session.txt"

# Cargar sesión si existe, si no, crear una nueva
if os.path.exists(TELEGRAM_SESSION_FILE):
    with open(TELEGRAM_SESSION_FILE, "r") as file:
        string_session = file.read().strip()
        print("Session loaded from file.")
else:
    string_session = None

SESSION_NAME = StringSession(string_session)

async def iniciar_sesion():
    async with TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH) as client:
        print("Authentication successful!")
        if not string_session:
            nueva_sesion = client.session.save()
            with open(TELEGRAM_SESSION_FILE, "w") as file:
                file.write(nueva_sesion)
            print("Session saved to file.")

        print("Your String session:", client.session.save())

# Ejecutar autenticación
with TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH) as client:
    client.loop.run_until_complete(iniciar_sesion())