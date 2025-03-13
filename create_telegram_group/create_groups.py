import os
from quart import Quart, request, jsonify
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import CreateChatRequest, ExportChatInviteRequest

# Custom modules
import constants



# Get group ID
async def get_group_id(client, group_name):
    """ 
    Finds the group ID in the user dialogues and sorts by creation date 
    
    Nota: Esta implementación no es la más precisa, ya que simplemente filtra los chats 
    del usuario autenticado y devuelve el grupo más reciente con el mismo nombre.

    De momento no he encontrado otra forma de obtener el group ID.
    """
    dialogs = await client.get_dialogs()
    grupos = [dialog for dialog in dialogs if dialog.title == group_name]
    if not grupos:
        return None
    grupos.sort(key=lambda g: g.date, reverse=True)
    return grupos[0].id


# Load session from file
if os.path.exists(constants.TELEGRAM_SESSION_FILE):
    with open(constants.TELEGRAM_SESSION_FILE, "r") as file:
        string_session = file.read().strip()
        print("Session loaded from file.")
else:
    print("Session file not found. Run authentication first.")
    exit(1)


# Start Telethon Client with loaded session
client = TelegramClient(StringSession(string_session), constants.TELEGRAM_API_ID, constants.TELEGRAM_API_HASH)


# Start Quart
app = Quart(__name__)

@app.before_serving
async def startup():
    """ Starting the Telethon client at server startup """
    await client.connect()
    if not await client.is_user_authorized():
        print("The session is not authorised. Run authentication first.")
        exit(1)
    print("Telethon successfully started.")

@app.route('/create_group', methods=['POST'])
async def create_group():
    """ Create a group on Telegram """
    try:
        data = await request.get_json()
        group_name = data.get("group_name")

        if not group_name:
            return jsonify({"error": "'group_name' is required"}), 400

        # Create group with authenticated user
        await client(CreateChatRequest(users=[], title=group_name))

        # Group ID
        group_id = await get_group_id(client, group_name)
        if group_id is None:
            return jsonify({"error": "Group ID could not be obtained."}), 500
        
        # Generate the invitation link
        invitation = await client(ExportChatInviteRequest(group_id))

        return jsonify({
            "group_id": group_id,
            "group_name": group_name,
            "invite_link": invitation.link
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Execute Quart
if __name__ == '__main__':
    app.run(debug=True)
