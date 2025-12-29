from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Ayush import app


def help_pannel(_, START: Union[bool, int] = None):

    control_button = [
        InlineKeyboardButton(text="◁", callback_data="settings_back_helper_fixed"),
        InlineKeyboardButton(text="HOME", callback_data="settingsback_helper"),
        InlineKeyboardButton(text="▷", callback_data="aayuxaaru"),
    ]

    back_or_close = (
        [InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settings_back_helper")]
        if START
        else [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")]
    )

    menu = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1"),
                InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2"),
                InlineKeyboardButton(text=_["H_B_3"], callback_data="help_callback hb3"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_4"], callback_data="help_callback hb4"),
                InlineKeyboardButton(text=_["H_B_5"], callback_data="help_callback hb5"),
                InlineKeyboardButton(text=_["H_B_6"], callback_data="help_callback hb6"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_7"], callback_data="help_callback hb7"),
                InlineKeyboardButton(text=_["H_B_8"], callback_data="help_callback hb8"),
                InlineKeyboardButton(text=_["H_B_9"], callback_data="help_callback hb9"),
            ],
            control_button,
            back_or_close,
        ]
    )
    return menu


def help_back_markup(_):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settings_back_helper")]]
    )


def private_help_panel(_):
    return [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{app.username}?start=help",
            )
        ]
  ]
