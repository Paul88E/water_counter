from aiogram.filters.state import State, StatesGroup

from utils import WaterValue


class FSMWaterCounter(StatesGroup):
    waiting_for_values = State()
    waiting_for_checking = State()
    current_values: WaterValue | None
