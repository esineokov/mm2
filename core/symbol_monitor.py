import asyncio
import traceback

from prometheus_client import Counter

from core.strategy.base import Strategy
from core.trading_context import TradingContext

MONITOR_ERRORS = Counter("monitor_errors_total", "Total number of monitoring errors")
MONITOR_COUNTER = Counter("monitor_total", "Total number of monitor cycles")


class SymbolMonitor:
    def __init__(self, context: TradingContext, strategy: Strategy):
        self.context: TradingContext = context
        self.strategy: Strategy = strategy

    async def monitor(self, cycle_timeout_s: int = 1, notify_timeout_s: int = 1):
        while True:
            try:
                if await self.strategy.check_conditions():
                    await self.strategy.notify(notify_timeout_s)
            except Exception as e:
                MONITOR_ERRORS.inc()
                traceback.print_exc()
                print(e)
            finally:
                MONITOR_COUNTER.inc()
                await asyncio.sleep(cycle_timeout_s)
