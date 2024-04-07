from random import randrange
import enum


class State(enum.Enum):
    LOGIN = 1
    GAME_SESSION = 2
    STOP = 3


options = ('CREDITS', 'ALL_ITEMS', 'MY_ITEMS', 'BUY_ITEM', 'SELL_ITEM', 'LOGOUT')

delta_credits = randrange(1, 10)

items = {
    'destroyer': 20,
    'corvette': 30,
    'battleship': 40,
    'repair_team': 3,
    'gun': 4,
    'super_gun': 5
}
