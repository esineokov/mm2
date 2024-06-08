from enum import Enum

from aiogram.filters.callback_data import CallbackData


class Action(str, Enum):
    create = "create"


class CreateCallbackData(CallbackData, prefix="bot", sep="/"):
    action: Action
    symbol: str
    timeframe: str
    strategy_code: str
    index: str
