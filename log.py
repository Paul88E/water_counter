from datetime import datetime
from os import path

from input_data import WaterValue

LOG_NAME = 'log.txt'

Sent = True
Not_sent = False
Was_sent = Sent | Not_sent


def write_log(values: WaterValue) -> None:
    """ Writes date and values to log """
    record = _check_log_and_records() * '\n' + str(
        {'date': str(datetime.now().date()), 'text': values})
    if not sent_this_month():
        with open(LOG_NAME, 'a') as file:
            file.write(record)


def sent_this_month() -> Was_sent:
    """ Checks if the data have sent this month already """
    _check_log_and_records()
    with open(LOG_NAME, 'r') as file:
        if path.getsize(LOG_NAME) == 0:
            return Not_sent
        else:
            for last_record in file:
                pass
            try:
                last_record_dict = eval(last_record)
                if last_record_dict['date'][:7] == str(datetime.now().date())[:7]:
                    print('В этом месяце данные уже направлялись.')
                    return Sent
                else:
                    return Not_sent
            except SyntaxError:
                return Not_sent


def _check_log_and_records() -> bool:
    """ Checks log-file for existence and past records.
    Creates file if it is missing.
    Returns True if file have past records.
    Returns False if file haven't existed or had no records """
    if not path.isfile(LOG_NAME):
        with open(LOG_NAME, 'w'):
            print('Log-file created...')
            pass
        return False
    elif path.getsize(LOG_NAME) == 0:
        return False
    else:
        return True


if __name__ == '__main__':
    # LOG_NAME = 'test.log'
    # values2 = WaterValue(HOT_KITCHEN=1, COLD_KITCHEN=2, HOT_BATH=3, COLD_BATH=4)
    # write_log(values2)
    pass
