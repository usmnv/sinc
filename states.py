from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    waiting_phone = State()
    waiting_city = State()
    waiting_goal = State()

class CitySearch(StatesGroup):
    waiting_city_name = State()

class ExchangeState(StatesGroup):
    waiting_from_currency = State()
    waiting_to_currency = State()
    waiting_amount = State()
