import os
import asyncio
from quart import Quart, request, jsonify
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import CreateChatRequest, ExportChatInviteRequest

# Load environment variables
TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID", 0))
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH", "")
TELEGRAM_SESSION = os.getenv("TELEGRAM_SESSION", "")

# Get group ID
async def get_group_id(client, group_name):
    dialogs = await client.get_dialogs()
    grupos = [dialog for dialog in dialogs if dialog.title == group_name]
    if not grupos:
        return None
    grupos.sort(key=lambda g: g.date, reverse=True)
    return grupos[0].id

# Start Telethon Client with loaded session
client = TelegramClient(StringSession(TELEGRAM_SESSION), TELEGRAM_API_ID, TELEGRAM_API_HASH)

# Start Quart
app = Quart(__name__)

@app.before_serving
async def startup():
    await client.connect()
    if not await client.is_user_authorized():
        print("The session is not authorised. Run authentication first.")
        exit(1)
    print("Telethon successfully started.")

@app.route('/create_group', methods=['POST'])
async def create_group():
    try:
        data = await request.get_json()
        group_name = data.get("group_name")

        if not group_name:
            return jsonify({"error": "'group_name' is required"}), 400

        await client(CreateChatRequest(users=[], title=group_name))

        group_id = await get_group_id(client, group_name)
        if group_id is None:
            return jsonify({"error": "Group ID could not be obtained."}), 500

        invitation = await client(ExportChatInviteRequest(group_id))

        return jsonify({
            "group_id": group_id,
            "group_name": group_name,
            "invite_link": invitation.link
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.run(debug=True, host="0.0.0.0", port=5000))