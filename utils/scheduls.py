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
    """ Sends values to service company, if they weren't sent by user """
    if not sent_this_month():
        generated_values = generate_values()
        if send_data(generated_values.values, CHOSEN_SERVICE):
            await _send_generated_values_was_sent_message(generated_values, bot)
            write_log(generated_values)


async def _schedule_sender_generated_values(scheduler: AsyncIOScheduler, bot: Bot):
    """ Schedule, that starts in last day of sending period and starts sending function """
    now = datetime.now()
    scheduler_start_time = datetime(year=now.year,
                                    month=now.month,
                                    day=int(bot_config.reminder["last_day"]),
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
    """ Checks day of running bot in month, creates every-month-schedule,
    which generates schedule of sending values to service company """
    if datetime.now().day == int(bot_config.reminder["last_day"]):
        await _schedule_sender_generated_values(scheduler, bot)
    scheduler.add_job(_schedule_sender_generated_values,
                      trigger='cron',
                      day=int(bot_config.reminder["last_day"]),
                      args=(scheduler, bot)
                      )


async def schedule_reminder_to_send_values(scheduler: AsyncIOScheduler, bot: Bot):
    """ Schedule, that sends user message with reminding about sending
     water values to service company """
    scheduler.add_job(_send_reminder_message,
                      trigger='cron',
                      day=bot_config.reminder['days'],
                      hour=bot_config.reminder['hours'],
                      minute=bot_config.reminder['minutes'],
                      args=(bot,)
                      )


async def schedulers_pack(bot: Bot):
    """ Creates two schedules: reminder and schedule,
    that creates another schedule, which sends values """
    scheduler: AsyncIOScheduler = AsyncIOScheduler(
        timezone=str(tzlocal.get_localzone()))
    await schedule_reminder_to_send_values(scheduler, bot)
    await schedule_month_schedule_creator(scheduler, bot)
    scheduler.start()
    scheduler.print_jobs()
