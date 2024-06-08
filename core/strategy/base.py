from abc import ABC
from threading import RLock

from aiogram.utils.keyboard import InlineKeyboardBuilder
from prometheus_client import Summary

from core.condition.base import Condition
from core.models.bot_callback import CreateCallbackData, Action
from core.trading_context import TradingContext
from datetime import datetime, timezone, timedelta
from io import BytesIO

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BufferedInputFile,
)
from pandas import DataFrame
import mplfinance as mpf

from config import env

CHECK_CONDITIONS_DURATION = Summary("check_conditions_duration", "Time spent checking conditions")
NOTIFY_DURATION = Summary("notify_duration", "Time spent notifying")


class Strategy(ABC):
    def __init__(self, context: TradingContext, conditions: list[Condition], lock: RLock, bot):
        self.context: TradingContext = context
        self.conditions: list[Condition] = conditions
        self.last_notify_datetime = None
        self.lock = lock
        self.bot = bot

        self.caption = "CAPTION_TEMPLATE"
        self.code = "CODE_TEMPLATE"

    @CHECK_CONDITIONS_DURATION.time()
    async def check_conditions(self, data: DataFrame | None = None) -> bool:
        data: DataFrame = self.context.get_data() if data is None else data
        for condition in self.conditions:
            result: bool = await condition.check(data)
            if not result:
                return False
        return True

    @NOTIFY_DURATION.time()
    async def notify(self, notify_timeout_s: int, data: DataFrame | None = None):
        data: DataFrame = await self.context.get_data() if data is None else data
        current_time = datetime.now(tz=timezone.utc)

        if self.last_notify_datetime and current_time - self.last_notify_datetime < timedelta(seconds=notify_timeout_s):
            return

        with self.lock:
            fig, ax = mpf.plot(
                data,
                type="candle",
                style="charles",
                title=f"{self.__class__.__name__} {self.context.symbol} {self.context.timeframe}",
                ylabel="Price",
                mav=(8, 20),
                show_nontrading=False,
                returnfig=True,
            )

            buf = BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)

        photo = BufferedInputFile(buf.getvalue(), filename="chart.png")

        builder = InlineKeyboardBuilder()
        builder.button(
            text="Create",
            callback_data=CreateCallbackData(
                action=Action.create,
                symbol=self.context.symbol,
                timeframe=str(self.context.timeframe),
                strategy_code=self.code,
                index=str(data.index[-1]),
            ),
        )
        #     inline_keyboard=[
        #         [
        #             InlineKeyboardButton(
        #                 text="Create",
        #                 callback_data=,
        #                 # callback_data=f"CREATE/{self.context.symbol}/{self.context.timeframe}/{self.callback_code}/{data.index[-1]}",
        #             )
        #         ]
        #     ]
        # )

        await self.bot.send_photo(env.int("CHAT_ID"), photo, caption=self.caption, reply_markup=builder.as_markup())
        self.last_notify_datetime = current_time
