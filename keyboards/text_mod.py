from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_text_mod_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Zalgo-текст", callback_data="zalgo")],
        [InlineKeyboardButton(text="Разделённый текст", callback_data="spaced")],
        [InlineKeyboardButton(text="Верхний регистр", callback_data="uppercase")],
        [InlineKeyboardButton(text="Fancy Font", callback_data="fancy")],
        [InlineKeyboardButton(text="Жирный текст", callback_data="bold")],
        [InlineKeyboardButton(text="Текст в изображение", callback_data="text_to_image")],
        [InlineKeyboardButton(text="Очистить", callback_data="clear")],
    ])
