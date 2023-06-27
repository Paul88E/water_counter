import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.fsm.storage.redis import RedisStorage
# from redis import Redis
# import aioredis
from config_data import bot_config
from keyboards import set_main_menu
from handlers import admin_router, not_admin_router


async def main():

    # redis = await aioredis.from_url("redis://localhost:6379", db=5)
    # redis: Redis = Redis(host='localhost')
    # storage: RedisStorage = RedisStorage(redis=redis)
    storage: MemoryStorage = MemoryStorage()

    bot: Bot = Bot(token=bot_config.tg_bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)
    await set_main_menu(bot)

    dp.include_router(not_admin_router)
    dp.include_router(admin_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
