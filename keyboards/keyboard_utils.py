from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon import LEXICON_KEYBOARDS

keyboard_check_and_send_values: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=
    [[InlineKeyboardButton(text=LEXICON_KEYBOARDS['send'],
                           callback_data='send'),
      InlineKeyboardButton(text=LEXICON_KEYBOARDS['change_values'],
                           callback_data='change_values'),
      InlineKeyboardButton(text=LEXICON_KEYBOARDS['cancel_sending'],
                           callback_data='cancel_sending')]]
)

keyboard_decreasing_values: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=
    [[InlineKeyboardButton(text=LEXICON_KEYBOARDS['change_values'],
                           callback_data='change_values'),
      InlineKeyboardButton(text=LEXICON_KEYBOARDS['cancel_sending'],
                           callback_data='cancel_sending')]]
)
