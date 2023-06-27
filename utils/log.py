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
        """ Returns True if all of values of other are equal or bigger, than
         equivalent values of self. If any value is less, returns False """
        for key in self.__dict__.keys():
            if self.__dict__[key] < other.__dict__[key]:
                return False
        return True

    def __lt__(self, other):
        """ Returns True if all of values of other are eqal or less, than
            equivalent values of self. If any value is bigger, returns False """
        for key in self.__dict__.keys():
            if self.__dict__[key] > other.__dict__[key]:
                return False
        return True

    def __eq__(self, other):
        """ Returns True if all of values of other are equal to
            equivalent values of self. If any value is less or bigger, returns False """
        for key in self.__dict__.keys():
            if self.__dict__[key] != other.__dict__[key]:
                return False
        return True


class LogWaterCounter:

    def __init__(self, log_name: str):
        self.log: dict[datetime, WaterValue] = {}
        self.log_name = log_name
        self._check_log_and_records()

    def __str__(self):
        line: str = ''
        for k, v in self.log.items():
            line += str(k.date()) + '\n' + str(v) + '\n'
        return line.rstrip('\n')

    def __repr__(self):
        line: str = ''
        for k, v in self.log.items():
            line += str(k.__str__()) + ': ' + str(v.__repr__()) + '\n'
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

    def _read(self) -> None:
        with open(self.log_name, 'r') as f:
            self.log: dict[datetime, WaterValue] = {}
            try:
                _log: dict[str, str] = json.load(f)
                for k, v in _log.items():
                    values = {}
                    for key, value in eval(v).items():
                        try:
                            values[key] = float(value)
                        except ValueError:
                            values[key] = None
                    self.log.update({datetime.fromisoformat(k): WaterValue(**values)})
            except (json.decoder.JSONDecodeError, TypeError):
                shutil.copyfile(self.log_name,
                                f'{self.log_name.split(".")[0]}_'
                                f'{str(datetime.now()).replace(":", "-")}'
                                f'.{self.log_name.split(".")[1]}')
                with open(self.log_name, 'w'):
                    pass

    def add(self, new_record: dict[datetime, WaterValue]) -> None:
        self.log.update(new_record)
        self.write()

    def write(self) -> None:
        print('log.write is achieved')
        _log: dict[str, str] = {}
        for k, v in self.log.items():
            _log.update({k.strftime(LOG_TIME_FORMAT): v.__repr__()})
        with open(self.log_name, 'w') as f:
            json.dump(_log, f)
            print('log is wrote')
