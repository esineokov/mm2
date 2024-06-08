import logging

from pandas import DataFrame

from core.condition.base import Condition


class BullishPinBarCondition(Condition):
    async def check(self, data: DataFrame | None = None):
        data: DataFrame = self.context.get_data() if data is None else data
        current = data.iloc[-1]

        high = current.high - current.low
        open = current.open - current.low
        close = current.close - current.low

        third = high / 3
        two_thirds = 2 * third

        self.log_info(
            f"""
            high: {high}
            open: {open}
            close: {close}
            third: {third}
            two_thirds: {two_thirds}
            """
        )

        result = close >= two_thirds and open >= two_thirds
        self.log_info(f"result: {result}")

        return result


class BearishPinBarCondition(Condition):
    async def check(self, data: DataFrame | None = None):
        data: DataFrame = self.context.get_data() if data is None else data
        current = data.iloc[-1]

        high = current.high - current.low
        open = current.open - current.low
        close = current.close - current.low

        third = high / 3

        self.log_info(
            f"""
            high: {high}
            open: {open}
            close: {close}
            third: {third}
            """
        )

        result = close <= third and open <= third
        self.log_info(f"result: {result}")

        return result
