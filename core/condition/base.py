import logging
from abc import ABC, abstractmethod
from core.trading_context import TradingContext


class Condition(ABC):
    def __init__(self, context: TradingContext):
        self.context = context

    @property
    def log_context(self) -> str:
        return f"[{self.__class__.__name__}][{self.context.symbol}][{self.context.timeframe}]"

    def log_info(self, msg, *args, **kwargs):
        self.log_info(f"{msg}", *args, **kwargs)

    @abstractmethod
    async def check(self, *args, **kwargs) -> bool:
        pass
