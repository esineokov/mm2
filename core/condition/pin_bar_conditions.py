from pandas import DataFrame

from core.condition.base import Condition


class BullishPinBarCondition(Condition):
    async def check(self):
        data: DataFrame = await self.context.get_data(count=1)
        current = data.iloc[-1]

        high = current.high - current.low
        open = current.open - current.low
        close = current.close - current.low

        third = high / 3
        two_thirds = 2 * third

        return close >= two_thirds and open >= two_thirds


class BearishPinBarCondition(Condition):
    async def check(self):
        data: DataFrame = await self.context.get_data(count=1)
        current = data.iloc[-1]

        high = current.high - current.low
        open = current.open - current.low
        close = current.close - current.low

        third = high / 3

        return close <= third and open <= third
