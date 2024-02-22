import csv
import os
from dataclasses import dataclass, fields, asdict
from typing import List

from slugify import slugify
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
    was_online: str | None = None

    @staticmethod
    def user_fields() -> list:
        return [field.name for field in fields(User)]


async def write_to_csv(file_name: str, users_list: List[User]) -> None:
    with open(
        f"{slugify(file_name)}-members.csv", "w", encoding="utf-8", newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=User.user_fields())

        writer.writeheader()
        for user in users_list:
            writer.writerow(asdict(user))


async def get_all_chat() -> list:
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
    return chats


async def choice_of_chat(chats: list):
    for i, chat in enumerate(chats):
        print(f"Index group: {i}; Name group: {chat.title}")
    print("*" * 100 + "\nChoose a group")

    group_numb = input("Enter index group: ")
    print("*" * 100 + "\nSTART")
    all_participants = await client.get_participants(
        chats[int(group_numb)], aggressive=True
    )
    return all_participants, chats[int(group_numb)].title


async def get_all_members_group(all_participants) -> List[User]:

    users_list = []
    for user in all_participants:
        try:
            was_online = user.status.was_online.strftime("%d-%m-%Y")
        except AttributeError:
            was_online = None
        users_list.append(
            User(
                id=user.id,
                username=user.username if user.username else None,
                first_name=user.first_name if user.first_name else None,
                last_name=user.last_name if user.last_name else None,
                phone=user.phone if user.phone else None,
                was_online=was_online,
            )
        )
    return users_list


async def main() -> None:
    chats = await get_all_chat()
    all_participants, chat_name = await choice_of_chat(chats)
    list_users = await get_all_members_group(all_participants)

    await write_to_csv(file_name=chat_name, users_list=list_users)
    print("All user scraped\n" + "*" * 100)


with client:
    client.loop.run_until_complete(main())
