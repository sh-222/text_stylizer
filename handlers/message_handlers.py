from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.states import TextStates
from keyboards.text_mod import get_text_mod_keyboard


router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    """
    Обработчик команды /start
    """
    await message.answer("Привет! Я могу изменить ваш текст несколькими способами. "
                        "Просто отправьте мне текст, и я предложу варианты его изменения.\n\n"
                        "Например: отправьте 'Привет' и попробуйте разные опции изменения текста.\n\n"
                        "Внимание! бот может обрабатывать только текстовые сообщения. длинной до 100 символов.\n\n")

@router.message(F.text)
async def process_text(message: Message, state: FSMContext):
    """Обработчик входящего текста для модификации"""
    text = message.text.strip()
    await state.set_state(TextStates.waiting_for_text)
    await state.update_data(text=text)
    
    await message.answer(
        "Выберите способ модификации:",
        reply_markup=get_text_mod_keyboard()
    )
