from aiogram.filters.state import State, StatesGroup

from utils import WaterValue


class FSMWaterCounter(StatesGroup):
    default_state = State()
    waiting_for_values = State()
    waiting_for_checking = State()
    current_values: WaterValue | None
