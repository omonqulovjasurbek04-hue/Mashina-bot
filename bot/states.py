from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):
    search = State()
    compare = State()
    ask = State()
