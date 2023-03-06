from dataclasses import dataclass


@dataclass
class WaterValue:
    """ Class to contain values of water meters """
    HOT_KITCHEN: float
    HOT_BATH: float
    COLD_KITCHEN: float
    COLD_BATH: float

    def __repr__(self):
        return f'{self.__dict__}'


def _check_float(row: list[str]) -> bool:
    """ Check input string for float values form """
    for part in row:
        try:
            float(part)
        except ValueError:
            return False
    return True


def _checked_input() -> list[float] | None:
    """ Returns input string, which fit to row of 4 float numbers """
    row = []
    while not row:
        if row is None:
            print('Прекратить ввод данных можно введя любую строку без пробелов.')
        text = input('Введите показания четырех счетчиков воды в '
                     'любом порядке через пробел\n'
                     '(допускается и десятичная точка и запятая):\n')
        # text = '27.9 55.0 179.5 130.2'
        n = len(text.split())
        match n:
            case 0 | 1:  # to end cycle with any single word
                print('Работа программы прекращена вашим запросом без пробелов.')
                return None
            case 4:
                row = text.replace(',', '.').split()
                if _check_float(row):
                    return [float(f) for f in row]
                else:
                    print('Введенные данные не являются числами. Введите корректные данные.')
                    row = None
            case _:
                print(f'Введено {n} показаний счетчиков, а нужно 4.')
                row = None


def safe_input() -> WaterValue | None:
    row = _checked_input()
    if row is None:
        return None
    else:
        row.sort()
        return WaterValue(HOT_KITCHEN=row[0], COLD_KITCHEN=row[1],
                          HOT_BATH=row[2], COLD_BATH=row[3])


if __name__ == '__main__':
    pass
