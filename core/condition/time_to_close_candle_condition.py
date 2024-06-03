from datetime import datetime, timezone, timedelta

from aiomql import TimeFrame
from pandas import DataFrame

from core.condition.base import Condition

timedelta_dict = {
    TimeFrame.M1: timedelta(minutes=1),
    TimeFrame.M5: timedelta(minutes=5),
    TimeFrame.M15: timedelta(minutes=15),
    TimeFrame.M30: timedelta(minutes=30),
    TimeFrame.H1: timedelta(hours=1),
    TimeFrame.H4: timedelta(hours=4),
    TimeFrame.D1: timedelta(days=1),
    TimeFrame.W1: timedelta(weeks=1),
    TimeFrame.MN1: timedelta(weeks=4),
}


class TimeUntilCandleCloseCondition(Condition):
    def __init__(self, delta: timedelta, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delta = delta

    async def check(self):
        data: DataFrame = await self.context.get_data(count=2)

        current_time: datetime = datetime.now(tz=timezone.utc)
        candle_start_time: datetime = data.index[-1].to_pydatetime()
        candle_start_time: datetime = candle_start_time.replace(tzinfo=timezone.utc)
        candle_end_time: datetime = candle_start_time + timedelta_dict[self.context.timeframe]
        current_delta: timedelta = candle_end_time - current_time

        return current_delta.total_seconds() > 0 and current_delta <= self.delta
