import random

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import tzlocal
from datetime import datetime

from aiogram import Bot

from lexicon import LEXICON
from config_data import bot_config, CHOSEN_SERVICE, \
    HOURS_OF_SENDING_GENERATED_VALUES
from utils import generate_values, sent_this_month, write_log
from services import send_data


async def _send_reminder_message(bot: Bot):
    await bot.send_message(chat_id=bot_config.admin_ids[0],
                           text=LEXICON['remind_to_send_values'])


async def _send_generated_values_was_sent_message(generated_values,
                                                  bot: Bot):
    await bot.send_message(chat_id=bot_config.admin_ids[0],
                           text=LEXICON['generated_values_were_sent']
                           + '\n' + generated_values.__repr__()
                           )


async def _send_generated_values(bot: Bot):
    if not sent_this_month():
        generated_values = generate_values()
        if send_data(generated_values.values, CHOSEN_SERVICE):
            await _send_generated_values_was_sent_message(generated_values, bot)
            write_log(generated_values)


async def _schedule_sender_generated_values(scheduler: AsyncIOScheduler, bot: Bot):
    scheduler_start_time = datetime(year=datetime.now().year,
                                    month=datetime.now().month,
                                    day=datetime.now().day,
                                    hour=random.randrange(HOURS_OF_SENDING_GENERATED_VALUES[0],
                                                          HOURS_OF_SENDING_GENERATED_VALUES[1] + 1),
                                    minute=random.randrange(0, 59),
                                    second=random.randrange(0, 59))
    scheduler.add_job(_send_generated_values,
                      trigger='date',
                      run_date=scheduler_start_time,
                      args=(bot,)
                      )
    scheduler.print_jobs()


async def schedule_month_schedule_creator(scheduler: AsyncIOScheduler, bot: Bot):
    """ Every month creates schedule, which generates values and send it by mail """
    scheduler.add_job(_schedule_sender_generated_values,
                      trigger='cron',
                      day='1',
                      args=(scheduler, bot,)
                      )


async def schedule_reminder_to_send_values(scheduler: AsyncIOScheduler, bot: Bot):
    scheduler.add_job(_send_reminder_message,
                      trigger='cron',
                      day=bot_config.reminder['days'],
                      hour=bot_config.reminder['hours'],
                      minute=bot_config.reminder['minutes'],
                      args=(bot,)
                      )


async def schedulers_pack(bot: Bot):
    scheduler: AsyncIOScheduler = AsyncIOScheduler(
        timezone=str(tzlocal.get_localzone()))
    await schedule_reminder_to_send_values(scheduler, bot)
    await schedule_month_schedule_creator(scheduler, bot)
    scheduler.start()
    scheduler.print_jobs()
