import datetime
from dataclasses import dataclass

from lexicon import LEXICON
from .log import WaterValue, LogWaterCounter
from config_data import LOG_NAME

Sent = True
Not_sent = False
Was_sent = Sent | Not_sent
Increase = True
Decrease = False
Compeared = Increase | Decrease

log: LogWaterCounter = LogWaterCounter(LOG_NAME)


@dataclass
class Response:
    """ Class contains values and text with response """
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


def _sent_this_month() -> Was_sent:
    """ Checks if the data have sent this month already """
    if len(log.log) > 0:
        last_date = max(log.log.keys()).date()
        if last_date == datetime.datetime.now().date():
            return Sent
    return Not_sent


def _check_values_to_increase(values: WaterValue) -> Compeared:
    """ Checks if new values are bigger or equal than last ones from log.
        Returns Increase(True) is they're bigger or equal and Decrease(False) if not."""
    if len(log.log) > 0:
        last_date = max(log.log.keys())
        if log.log[last_date] > values:
            return Decrease
    return Increase


def correct_input(text: str) -> Response:
    row: list[float | None] = list(
        _checked_float(text.replace(',', '.').split()))
    values: WaterValue | None = None
    if all(row) and len(row) == 4:  # four float values added
        row.sort()
        values = WaterValue(HOT_KITCHEN=row[0], COLD_KITCHEN=row[1],
                            HOT_BATH=row[2], COLD_BATH=row[3])
        if _sent_this_month():
            answer = LEXICON['sent_this_month_already'] + '\n' + \
                     '<i>' + LEXICON['repeat_sending_by_mistake'] + '</i>'
        else:
            if _check_values_to_increase(values):
                answer = LEXICON['correct_values']
            else:
                answer = LEXICON['decreasing_values']
    elif not all(row) and len(row) != 4:
        answer = LEXICON['wrong_values'] + ' '\
                 + f"{len(row)} {LEXICON['wrong_number_of_values']}"
    elif not all(row):
        answer = LEXICON['wrong_values']
    else:  # len(row) != 4:
        answer = f"{len(row)} {LEXICON['wrong_number_of_values']}"
    return Response(VALUES=values, RESPONSE=answer)


def write_log(values: WaterValue):
    log.add({datetime.datetime.now(): values})
