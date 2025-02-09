from aiogram import F, Router
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.reply(f"Привет {message.from_user.full_name}")


# ---------------------------------------------------------------------------- #


@router.message(F.content_type == ContentType.TEXT)
async def message_handler(message: Message):
    await message.reply(message.text)  # type: ignore
