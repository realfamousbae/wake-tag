from logging import Logger
from telethon import TelegramClient
from telethon.events import NewMessage

from .config import Config

from asyncio import sleep
from os import environ
from re import escape

from telethon.errors import ChatAdminRequiredError, FloodWaitError

MAX_USERS = 500
MENTIONS_PER_MESSAGE = 50


async def _get_users(client: TelegramClient, group_id: int, author_id: int, self_id: int) -> list:
    members = []

    async for user in client.iter_participants(group_id):
        if not user.deleted and not user.bot and user.id not in (self_id, author_id):
            members.append(user)

    return members


def _mention(user) -> str:
    if user.username:
        return f"@{user.username}"

    name = (user.first_name or "user").replace("[", "").replace("]", "")
    return f"[{name}](tg://user?id={user.id})"


def _chunks(mentions: list[str], limit: int = 3500, per_message: int = MENTIONS_PER_MESSAGE) -> list[str]:
    result, current, count = [], "", 0

    for mention in mentions:
        if current and (len(current) + len(mention) + 1 > limit or count >= per_message):
            result.append(current)
            current, count = "", 0
        current += mention + " "
        count += 1

    if current:
        result.append(current)
    return result


class TelegramBot:
    def __init__(self, logger: Logger, config: Config) -> None:
        self.logger = logger
        self.config = config

        self.client = TelegramClient(
            environ.get("SESSION_PATH", "bot"),
            self.config["tech"]["api_id"],
            self.config["tech"]["api_hash"]
        )

    async def handlers(self) -> None:
        self.me = await self.client.get_me()

        @self.client.on(NewMessage(incoming=True, func=lambda c: c.is_private))
        async def empty_message(event) -> None:
            if not (event.raw_text or "").startswith(("/help", "/start")):
                await event.client.send_message(
                    event.chat_id,
                    "Для взаимодействия используйте команды /start и /help."
                )
                
        @self.client.on(NewMessage(pattern="^/all$", incoming=True, func=lambda c: c.is_group))
        @self.client.on(NewMessage(pattern=f"^/all@{escape(self.me.username)}$", incoming=True, func=lambda c: c.is_group))
        async def all_tag(event) -> None:
            try:
                users = await _get_users(self.client, event.chat_id, event.sender_id, self.me.id)
            except ChatAdminRequiredError:
                return await event.reply("Чтобы упоминать участников, мне нужны права администратора в этом чате.")

            if len(users) > MAX_USERS:
                return await event.reply(
                    f"К сожалению я пока не могу упоминать всех участников группового чата, "
                    f"если их число превышает {MAX_USERS} человек. Следите за новостями, функционал бота постоянно расширяется!"
                )

            if not users:
                return

            for i, chunk in enumerate(_chunks([_mention(user) for user in users])):
                try:
                    await (event.reply(chunk) if i == 0 else event.respond(chunk))
                except FloodWaitError as error:
                    await sleep(error.seconds)
                    await event.respond(chunk)
                await sleep(1)

        @self.client.on(NewMessage(pattern="^/start$", incoming=True))
        @self.client.on(NewMessage(pattern=f"^/start@{escape(self.me.username)}$", incoming=True))
        async def start_command(event) -> None:
            await event.client.send_message(
                event.chat_id,
                """Привет, я позволяю реализовать функционал тега /all в групповых чатах Telegram. 
Добавь меня в группу и начни пользоваться всеми функциями.

Для инструкций используйте /help."""
            )
        
        @self.client.on(NewMessage(pattern="^/help$", incoming=True))
        @self.client.on(NewMessage(pattern=f"^/help@{escape(self.me.username)}$", incoming=True))
        async def help_command(event) -> None:
            await event.client.send_message(
                event.chat_id,
                """Используйте команду `/all` чтобы упомянуть всех участников в любом групповом чате."""
            )

    async def run(self) -> None:
        self.logger.info("Bot starts his work.")
        await self.client.run_until_disconnected()
