import asyncio
import logging
import threading
from datetime import timedelta

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiomql import MetaTrader, TimeFrame
from prometheus_client import start_http_server, Gauge

from config import env
from core.condition.ring_high_low_condition import RingLowCondition, RingHighCondition
from core.condition.time_to_close_candle_condition import TimeUntilCandleCloseCondition
from core.condition.trend_conditions import UpTrendCondition, DownTrendCondition
from core.strategy.ring_high_low_strategies import RingLowStrategy, RingHighStrategy
from core.symbol_monitor import SymbolMonitor
from core.trading_context import TradingContext


logging.basicConfig(level=logging.DEBUG)
lock = threading.RLock()

mt5 = MetaTrader()


bot = Bot(token=env.str("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def symbol_activity_monitoring():
    symbol_trade_mode = Gauge("symbol_trade_mode", "Trade mode of symbols", ["symbol"])
    symbol_count = Gauge("symbol_count", "Total number of symbols")

    while True:
        try:
            symbols = await mt5.symbols_get()
            symbol_count.set(len(symbols))
            for symbol in symbols:
                symbol_trade_mode.labels(symbol.name).set(symbol.trade_mode)
            await asyncio.sleep(60)
        except Exception as e:
            print(e)


async def main():
    task_queue = []

    await mt5.initialize(
        login=env.int("MT5_LOGIN"),
        password=env.str("MT5_PASSWORD"),
        server=env.str("MT5_SERVER"),
    )

    task_queue.append(dp.start_polling(bot))
    task_queue.append(symbol_activity_monitoring())

    symbols = await mt5.symbols_get()
    symbols = [s for s in symbols if s.trade_mode == 4]
    symbols = [
        s
        for s in symbols
        if str(s.name).startswith("USD") or str(s.name).endswith("USD") or str(s.name).endswith("USDm")
    ]

    for symbol in symbols:
        for timeframe in [TimeFrame.D1, TimeFrame.H4]:

            context: TradingContext = TradingContext(terminal=mt5, symbol=symbol.name, timeframe=timeframe)
            delta: timedelta = timedelta(minutes=5)

            up_trend_condition = UpTrendCondition(context=context)
            down_trend_condition = DownTrendCondition(context=context)

            ring_low_condition = RingLowCondition(context=context)
            ring_high_condition = RingHighCondition(context=context)

            time_until_candle_close_condition = TimeUntilCandleCloseCondition(context=context, delta=delta)

            rl_conditions = [time_until_candle_close_condition, up_trend_condition, ring_low_condition]
            rh_conditions = [time_until_candle_close_condition, down_trend_condition, ring_high_condition]

            rl_strategy = RingLowStrategy(bot=bot, lock=lock, context=context, conditions=rl_conditions)
            rl_monitor = SymbolMonitor(context=context, strategy=rl_strategy)
            rl_task = rl_monitor.monitor(cycle_timeout_s=60, notify_timeout_s=int(delta.total_seconds()))

            rh_strategy = RingHighStrategy(bot=bot, lock=lock, context=context, conditions=rh_conditions)
            rh_monitor = SymbolMonitor(context=context, strategy=rh_strategy)
            rh_task = rh_monitor.monitor(cycle_timeout_s=60, notify_timeout_s=int(delta.total_seconds()))

            task_queue.append(rl_task)
            task_queue.append(rh_task)

    await asyncio.gather(*task_queue)


if __name__ == "__main__":
    start_http_server(8000)
    asyncio.run(main(), debug=True)
