import datetime
from dataclasses import dataclass

from lexicon import LEXICON
from .log import WaterValue, LogStructure, LogWaterCounter
from config_data import LOG_NAME, GENERATED_DATA_SPREAD, REMINDER, \
    DEFAULT_VALUES_DELTA_PER_MONTH

Sent = True
Not_sent = False
Was_sent = Sent | Not_sent

log: LogWaterCounter = LogWaterCounter(LOG_NAME)


@dataclass
class Response:
    """ Class contains values and text of response """
    VALUES: WaterValue | None
    RESPONSE: str  # text of response


def _checked_float(row: list[str]) -> list[float | None]:
    """ Check input string for float values form """
    row: list[float | None]
    for part in row:
        try:
            yield float(part)
        except ValueError:
            yield None


def sent_this_month() -> Was_sent:
    """ Checks if the data have sent this month already """
    if len(log.log) > 0:
        last_month: str = max(log.log.keys()).date().isoformat()[0:7]
        if last_month == datetime.datetime.now().date().isoformat()[0:7]:
            return Sent
    return Not_sent


def check_right_days_of_sending() -> bool:
    """ Check date of sending for match with right period -
     mostly from 20 to 25 days of month (from constants.py) """
    first_day, last_day = (int(n) for n in REMINDER['days'].split('-'))
    if datetime.datetime.today().day in range(first_day, last_day + 1):
        return True
    else:
        return False


def _decreasing_message(old: WaterValue, new: WaterValue) -> str:
    answer = LEXICON['decreasing_values'] + '\n' + \
             'Предыдущие значения -> ' \
             '<b>Новые значения</b> (куб. м):'
    for line, key in zip(old.__str__().splitlines(), old.__dict__.keys()):
        answer += '\n' + line.replace(' куб. м', '') + \
                  '\t->\t' + f'<b>{str(new.__dict__[key])}</b>'
    return answer


def _check_values_to_increase(values: WaterValue) -> str:
    """ Checks if new values are bigger or equal than last ones from log.
        Returns correct-message if they're bigger or equal and decrease-message if not."""
    if len(log.log) > 0:
        last_date = max(log.log.keys())
        if not log.log[last_date].values < values:
            return _decreasing_message(log.log[last_date].values, values)
    return LEXICON['correct_values']


def correct_input(text: str) -> Response:
    row: list[float | None] = list(
        _checked_float(text.replace(',', '.').split()))
    values: WaterValue | None = None
    if all(row) and len(row) == 4:  # four float values added
        row.sort()
        values = WaterValue(HOT_KITCHEN=row[0], COLD_KITCHEN=row[1],
                            HOT_BATH=row[2], COLD_BATH=row[3])
        if sent_this_month():
            answer = LEXICON['sent_this_month_already'] + '\n' + \
                     '<i>' + LEXICON['repeat_sending_by_mistake'] + '</i>'
        else:
            answer = _check_values_to_increase(values)
    elif not all(row) and len(row) != 4:
        answer = LEXICON['wrong_values'] + ' ' \
                 + f"{len(row)} {LEXICON['wrong_number_of_values']}"
    elif not all(row):
        answer = LEXICON['wrong_values']
    else:  # len(row) != 4:
        answer = f"{len(row)} {LEXICON['wrong_number_of_values']}"
    return Response(VALUES=values, RESPONSE=answer)


def write_log(values: LogStructure):
    log.add({datetime.datetime.now(): values})


def history_representing() -> str:
    text = ''
    for date, values in log.log.items():
        text += f'<b>{date}</b>\n{values}\n'
    return text.rstrip('\n')


def _calculate_middle_delta() -> WaterValue:
    if len(log.log) == 0:
        return WaterValue(**DEFAULT_VALUES_DELTA_PER_MONTH)
    elif len(log.log) == 1:
        return list(log.log.values())[0].values
    months: float = (max(log.log.keys()) - min(log.log.keys())).days / 365 * 12 + 1
    last_values: WaterValue = list(log.log.values())[-1].values
    middle_values: dict[str, float] = {}
    for k, v in last_values.__dict__.items():
        middle_values[k] = round(v / months, 2)
    return WaterValue(**middle_values)


def generate_values() -> LogStructure:
    from random import randrange
    generated_delta = _calculate_middle_delta() * (1 + randrange(-GENERATED_DATA_SPREAD * 10,
                                                                 GENERATED_DATA_SPREAD * 10)
                                                   / 1000)
    if len(log.log) == 0:
        gen_values = round(generated_delta, 2)
    else:
        gen_values = round(list(log.log.values())[-1].values + generated_delta, 2)
    return LogStructure(values=gen_values, falsity=True)
