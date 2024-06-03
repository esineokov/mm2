from pandas import DataFrame

from core.condition.base import Condition


class RingLowCondition(Condition):
    async def check(self):
        data: DataFrame = await self.context.get_data(count=2)
        current = data.iloc[-1]
        previous = data.iloc[-2]
        return current.high < previous.high and current.low < previous.low


class RingHighCondition(Condition):
    async def check(self):
        data: DataFrame = await self.context.get_data(count=2)
        current = data.iloc[-1]
        previous = data.iloc[-2]
        return current.high > previous.high and current.low > previous.low
