MAIL_SMTP: dict[str, str] = {
    'GMAIL': 'smtp.gmail.com',
    'YANDEX': 'smtp.yandex.ru',
    'RAMBLER': 'smtp.rambler.ru',
    }
CHOSEN_SERVICE = 'YANDEX'

LOG_NAME = 'water_counter.log'
LOG_TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f%z'

REMINDER: dict = {
    'days': '20-25',
    'first_day': 20,
    'last_day': 25,
    'hours': 18,
    'minutes': 0,
}

HOURS_OF_SENDING_GENERATED_VALUES: tuple[int, ...] = (20, 23)

GENERATED_DATA_SPREAD = 5  # percent of delta values per month spread

DEFAULT_VALUES_DELTA_PER_MONTH: dict[str, float] = {'HOT_BATH': 2.01,
                                                    'HOT_KITCHEN': 0.44,
                                                    'COLD_BATH': 2.89,
                                                    'COLD_KITCHEN': 0.77}
