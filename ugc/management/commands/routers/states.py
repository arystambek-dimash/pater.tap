from aiogram.fsm.state import State, StatesGroup


class DistanceForm(StatesGroup):
    GET_DISTANCE = State()
