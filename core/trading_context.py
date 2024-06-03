from dataclasses import dataclass

import pandas as pd
from aiomql import MetaTrader, TimeFrame
from pandas import DataFrame


@dataclass
class TradingContext:
    terminal: MetaTrader
    timeframe: TimeFrame
    symbol: str

    async def get_data(self, count: int = 50) -> DataFrame:
        result = await self.terminal.copy_rates_from_pos(
            symbol=self.symbol, timeframe=self.timeframe, start_pos=0, count=count
        )
        df = DataFrame(result)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.set_index("time", inplace=True)
        return df
