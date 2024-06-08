from pandas import DataFrame

from core.condition.base import Condition


class RingCondition(Condition):
    async def check(self, data: DataFrame | None = None):
        raise NotImplementedError

    def get_current(self, data: DataFrame):
        result = data.iloc[-1]
        self.log_info(f"current: {result}")
        return result

    @staticmethod
    def get_previous(self, data: DataFrame):
        result = data.iloc[-2]
        self.log_info(f"previous: {result}")
        return result


class RingLowCondition(RingCondition):
    async def check(self, data: DataFrame | None = None):
        data: DataFrame = data or await self.context.get_data(count=2)

        current = self.get_current(data)
        previous = self.get_previous(data)

        result = current.high < previous.high and current.low < previous.low

        self.log_info(f"result: {result}")

        return result


class RingHighCondition(RingCondition):
    async def check(self, data: DataFrame | None = None):
        data: DataFrame = data or await self.context.get_data(count=2)

        current = self.get_current(data)
        previous = self.get_previous(data)

        result = current.high > previous.high and current.low > previous.low

        self.log_info(f"result: {result}")

        return result
