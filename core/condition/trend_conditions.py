import logging

from pandas import DataFrame

from core.condition.base import Condition


class TrendCondition(Condition):
    async def check(self, data: DataFrame | None = None):
        raise NotImplementedError

    @staticmethod
    def get_ema_fast(data: DataFrame):
        return data["close"].ewm(span=8, min_periods=8, adjust=False).mean()

    @staticmethod
    def get_ema_slow(data: DataFrame):
        return data["close"].ewm(span=20, min_periods=20, adjust=False).mean()

    def get_ema_fast_last(self, data: DataFrame):
        result: float = self.get_ema_fast(data).iloc[-1]
        self.log_info(f"ema_fast last: {result}")
        return result

    def get_ema_slow_last(self, data: DataFrame):
        result: float = self.get_ema_slow(data).iloc[-1]
        self.log_info(f"ema_slow last: {result}")
        return result


class UpTrendCondition(TrendCondition):
    async def check(self, data: DataFrame | None = None):
        data: DataFrame = data or await self.context.get_data()
        fast, slow = self.get_ema_fast_last(data), self.get_ema_slow_last(data)
        result = fast > slow

        self.log_info(f"result: {result}")
        return result


class DownTrendCondition(TrendCondition):
    async def check(self, data: DataFrame | None = None):
        data: DataFrame = data or await self.context.get_data()
        fast, slow = self.get_ema_fast_last(data), self.get_ema_slow_last(data)
        result = fast < slow

        self.log_info(f"result: {result}")
        return result
