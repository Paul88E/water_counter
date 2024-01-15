from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
# from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon import LEXICON
from utils import correct_input, history_representing, \
    write_log, check_right_days_of_sending, \
    Response
from keyboards import keyboard_check_and_send_values, keyboard_decreasing_values
from services import send_data
from config_data import CHOSEN_SERVICE
from states import FSMWaterCounter

router: Router = Router()


@router.message(CommandStart(), StateFilter(FSMWaterCounter.default_state))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/start'])
    await state.set_state(FSMWaterCounter.waiting_for_values)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['/help'])


@router.message(Command(commands='send'), StateFilter(FSMWaterCounter.default_state))
async def process_send_waiting_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/send'])
    await state.set_state(FSMWaterCounter.waiting_for_values)


@router.message(Command(commands='options'))
async def process_options_command(message: Message):
    await message.answer(text=LEXICON['/options'])


@router.message(Command(commands='history'))
async def process_history_command(message: Message):
    await message.answer(text=history_representing())


@router.message(Command(commands='status'))
async def process_history_command(message: Message, state: FSMContext):
    await message.answer(text=str(await state.get_state()))


@router.message(Command(commands='cancel'))
async def process_history_command(message: Message, state: FSMContext):
    await state.set_state(FSMWaterCounter.default_state)
    await message.answer(text=LEXICON['cancel'])


@router.message(StateFilter(FSMWaterCounter.default_state))
async def process_text_while_default_state(message: Message):
    await message.answer(text=LEXICON['/help'])


@router.message(~Text(startswith='/'),
                StateFilter(FSMWaterCounter.waiting_for_values))
async def process_check_data(message: Message, state: FSMContext):
    response: Response = correct_input(message.text)
    if response.VALUES:
        if not check_right_days_of_sending():
            await message.answer(text=LEXICON['wrong_days_of_sending'])
        if response.RESPONSE.splitlines()[0] == LEXICON['decreasing_values']:
            await message.answer(text=f'{response.RESPONSE}',
                                 reply_markup=keyboard_decreasing_values)
        else:
            await message.answer(text=f'{response.RESPONSE}\n{response.VALUES}',
                                 reply_markup=keyboard_check_and_send_values)
        FSMWaterCounter.current_values = response.VALUES
        await state.set_state(FSMWaterCounter.waiting_for_checking)
    else:
        await message.answer(response.RESPONSE)


@router.callback_query(Text(text='send'),
                       StateFilter(FSMWaterCounter.waiting_for_checking))
async def process_sending_letter(callback: CallbackQuery, state: FSMContext):
    if FSMWaterCounter.current_values:
        if send_data(FSMWaterCounter.current_values, CHOSEN_SERVICE):
            await callback.message.answer(text=LEXICON['data_is_sent'])
            write_log(FSMWaterCounter.current_values)
            FSMWaterCounter.current_values = None
        else:
            await callback.message.answer(
                text=LEXICON['error_sending'] + CHOSEN_SERVICE + '.')
    else:
        await callback.message.answer(text=LEXICON['error_with_data'])
    await callback.answer()
    await state.set_state(FSMWaterCounter.default_state)


@router.callback_query(Text(text='cancel_sending'),
                       StateFilter(FSMWaterCounter.waiting_for_checking))
async def process_cancel_sending(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['cancel_sending'])
    await callback.answer()
    await state.set_state(FSMWaterCounter.default_state)


@router.callback_query(Text(text='change_values'),
                       StateFilter(FSMWaterCounter.waiting_for_checking))
async def process_change_values(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['change_values'])
    await callback.answer()
    await state.set_state(FSMWaterCounter.waiting_for_values)


@router.message()
async def process_get_status_by_unknown_reason(message: Message, state: FSMContext):
    await message.answer(text=str(await state.get_state()))
