import asyncio
from aioredis import from_url

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from config_data import bot_config
from keyboards import set_main_menu
from handlers import admin_router, not_admin_router
from utils import schedulers_pack


async def main():

    redis = await from_url("redis://localhost:6379", db=5)
    storage: RedisStorage = RedisStorage(redis=redis)

    bot: Bot = Bot(token=bot_config.tg_bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)
    await set_main_menu(bot)

    dp.include_router(not_admin_router)
    dp.include_router(admin_router)

    await schedulers_pack(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
