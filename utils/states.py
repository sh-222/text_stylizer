from aiogram.fsm.state import StatesGroup, State

class TextStates(StatesGroup):
    waiting_for_text = State()
    waiting_for_modification = State()
