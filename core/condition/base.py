from abc import ABC, abstractmethod
from core.trading_context import TradingContext


class Condition(ABC):
    def __init__(self, context: TradingContext):
        self.context = context

    @abstractmethod
    async def check(self) -> bool:
        pass
