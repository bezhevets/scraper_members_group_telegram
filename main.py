import os

from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]


client = TelegramClient("anon", API_ID, API_HASH)


async def main():
    chats = []

    result = await client(
        GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=200,
            hash=0,
        )
    )

    chats.extend(result.chats)
    list_title = [chat.title for chat in chats]
    print(list_title)


with client:
    client.loop.run_until_complete(main())
