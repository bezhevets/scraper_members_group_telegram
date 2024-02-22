import os
from dataclasses import dataclass, fields
from pprint import pprint

from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]


client = TelegramClient("anon", API_ID, API_HASH)


@dataclass
class User:
    id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | int | None = None

    @staticmethod
    def user_fields() -> list:
        return [field.name for field in fields(User)]


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

    for i, chat in enumerate(chats):
        print(f"Index group: {i}; Name group: {chat.title}")
    print("*" * 100 + "\nChoose a group")

    group_numb = input("Enter index group: ")
    all_participants = await client.get_participants(
        chats[int(group_numb)], aggressive=True
    )

    print("*" * 100 + "\nSTART")

    users_list = []
    for user in all_participants:
        users_list.append(
            User(
                id=user.id,
                username=user.username if user.username else None,
                first_name=user.first_name if user.first_name else None,
                last_name=user.last_name if user.last_name else None,
                phone=user.phone if user.phone else None,
            )
        )

    pprint(users_list)


with client:
    client.loop.run_until_complete(main())
