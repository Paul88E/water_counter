from datetime import datetime
from os import path
import shutil
import json
from dataclasses import dataclass

from config_data import LOG_TIME_FORMAT


@dataclass
class WaterValue:
    """ Class to contain values of water meters """
    HOT_KITCHEN: float
    HOT_BATH: float
    COLD_KITCHEN: float
    COLD_BATH: float

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __str__(self) -> str:
        return f"ГВС (кухня) – \t{self.HOT_KITCHEN} куб. м\n" \
               f"ГВС (с/узел) – \t{self.HOT_BATH} куб. м\n" \
               f"ХВС (кухня) – \t{self.COLD_KITCHEN} куб. м\n" \
               f"ХВС (с/узел) – \t{self.COLD_BATH} куб. м"

    def __gt__(self, other):
        """ Returns True if all values of other are equal or bigger, than
         equivalent values of self. If any value is less, returns False """
        for key in self.__dict__.keys():
            if self.__dict__[key] < other.__dict__[key]:
                return False
        return True

    def __lt__(self, other):
        """ Returns True if all values of other are equal or less, than
            equivalent values of self. If any value is bigger, returns False """
        for key in self.__dict__.keys():
            if self.__dict__[key] > other.__dict__[key]:
                return False
        return True

    def __eq__(self, other):
        """ Returns True if all values of other are equal to
            equivalent values of self. If any value is less or bigger, returns False """
        for key in self.__dict__.keys():
            if self.__dict__[key] != other.__dict__[key]:
                return False
        return True

    def __add__(self, other):
        return WaterValue(HOT_BATH=self.HOT_BATH + other.HOT_BATH,
                          HOT_KITCHEN=self.HOT_KITCHEN + other.HOT_KITCHEN,
                          COLD_BATH=self.COLD_BATH + other.COLD_BATH,
                          COLD_KITCHEN=self.COLD_KITCHEN + other.COLD_KITCHEN
                          )

    def __sub__(self, other):
        return WaterValue(HOT_BATH=self.HOT_BATH - other.HOT_BATH,
                          HOT_KITCHEN=self.HOT_KITCHEN - other.HOT_KITCHEN,
                          COLD_BATH=self.COLD_BATH - other.COLD_BATH,
                          COLD_KITCHEN=self.COLD_KITCHEN - other.COLD_KITCHEN
                          )

    def __mul__(self, other: int | float):
        return WaterValue(HOT_BATH=self.HOT_BATH * other,
                          HOT_KITCHEN=self.HOT_KITCHEN * other,
                          COLD_BATH=self.COLD_BATH * other,
                          COLD_KITCHEN=self.COLD_KITCHEN * other
                          )

    def __truediv__(self, other: int | float):
        if other == 0:
            return self
        else:
            return WaterValue(HOT_BATH=self.HOT_BATH / other,
                              HOT_KITCHEN=self.HOT_KITCHEN / other,
                              COLD_BATH=self.COLD_BATH / other,
                              COLD_KITCHEN=self.COLD_KITCHEN / other
                              )

    def __round__(self, n=None):
        return WaterValue(HOT_BATH=round(self.HOT_BATH, n),
                          HOT_KITCHEN=round(self.HOT_KITCHEN, n),
                          COLD_BATH=round(self.COLD_BATH, n),
                          COLD_KITCHEN=round(self.COLD_KITCHEN, n)
                          )


@dataclass
class LogStructure:
    values: WaterValue
    falsity: bool

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __str__(self) -> str:
        return f"{'fake: ' if self.falsity else ''}" \
               f"{self.values.__str__()}"


class LogWaterCounter:
    # dict[datetime, LogStructure]
    def __init__(self, log_name: str):
        self.log: dict[datetime, LogStructure] = {}
        self.log_name = log_name
        self._check_log_and_records()

    def __str__(self):
        line: str = ''
        for k, v in self.log.items():
            line += str(k.date()) + '\n' + str(v.values) + '\n'
        return line.rstrip('\n')

    def __repr__(self):
        line: str = ''
        for k, v in self.log.items():
            line += str(k.__str__()) + ': ' + str(v.values.__repr__()) + '\n'
            if v.falsity:
                line = 'fake: ' + line
        return line.rstrip('\n')

    def __getitem__(self, key):
        return self.log[key]

    def _check_log_and_records(self) -> None:
        """ Checks log-file for existence and past records.
        Creates file if it is missing.
        Returns True if file have past records.
        Returns False if file haven't existed or had no records """
        if not path.isfile(self.log_name):
            with open(self.log_name, 'w'):
                pass
        elif path.getsize(self.log_name) == 0:
            pass
        else:
            self._read()

    def _create_an_empty_file(self) -> None:
        shutil.copyfile(self.log_name,
                        f'{self.log_name.split(".")[0]}_'
                        f'{str(datetime.now()).replace(":", "-")}'
                        f'.{self.log_name.split(".")[1]}')
        with open(self.log_name, 'w'):
            pass

    def _read(self) -> None:

        def _load_log_structure(line: str) -> LogStructure | None:
            try:
                log_structure_dict = eval(line)
                return LogStructure(values=WaterValue(**log_structure_dict['values']),
                                    falsity=log_structure_dict['falsity'])
            except (SyntaxError, TypeError):
                return None

        def _datetime_parser(line: str) -> datetime | None:
            try:
                return datetime.fromisoformat(line)
            except ValueError:
                return None

        with open(self.log_name, 'r') as f:
            self.log: dict[datetime, LogStructure] = {}

            try:
                _log: dict[str, str] = json.load(f)  # load dict[datetime_str, LogStructure_str]
            except json.decoder.JSONDecodeError:
                self._create_an_empty_file()
                return None

        for datetime_str, values_and_falsity_dict_str in _log.items():
            time_: datetime | None = _datetime_parser(datetime_str)
            data_: LogStructure | None = _load_log_structure(values_and_falsity_dict_str)
            if time_ and data_:
                self.log.update({time_: data_})

    def add(self, new_record: dict[datetime, LogStructure]) -> None:
        self.log.update(new_record)
        self.write()

    def write(self) -> None:
        _log: dict[str, str] = {}
        for k, v in self.log.items():
            _log.update({k.strftime(LOG_TIME_FORMAT): v.__repr__()})
        with open(self.log_name, 'w') as f:
            json.dump(_log, f)
