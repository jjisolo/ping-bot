from aiogram.dispatcher.filters.state   import State, StatesGroup

class track_ip_form(StatesGroup):
    adress  = State()

class untrack_ip_form(StatesGroup):
    adress = State()
