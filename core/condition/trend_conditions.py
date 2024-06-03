from pandas import DataFrame

from core.condition.base import Condition


class UpTrendCondition(Condition):
    async def check(self):
        data: DataFrame = await self.context.get_data()
        ema_fast = data["close"].ewm(span=8, min_periods=8, adjust=False).mean()
        ema_slow = data["close"].ewm(span=20, min_periods=20, adjust=False).mean()
        return ema_fast.iloc[-1] > ema_slow.iloc[-1]


class DownTrendCondition(Condition):
    async def check(self):
        data: DataFrame = await self.context.get_data()
        ema_fast = data["close"].ewm(span=8, min_periods=8, adjust=False).mean()
        ema_slow = data["close"].ewm(span=20, min_periods=20, adjust=False).mean()
        return ema_fast.iloc[-1] < ema_slow.iloc[-1]
