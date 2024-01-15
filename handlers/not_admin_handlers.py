from aiogram import Router
from aiogram.types import Message

from filters import NotAdmin
from config_data import bot_config
from lexicon import LEXICON

router: Router = Router()


@router.message(NotAdmin(bot_config.admin_ids))
async def process_check_data(message: Message):
    await message.answer(text=LEXICON['not_your_bot'])
