# from aiomql import MetaTrader, SymbolInfo
#
# from core.condition.base import Condition
#
#
# class SymbolActiveCondition(Condition):
#     def __init__(self, terminal: MetaTrader, symbol: str):
#         self.terminal = terminal
#         self.symbol = symbol
#
#     async def check(self):
#         symbol_info: SymbolInfo | None = await self.terminal.symbol_info(self.symbol)
#         return symbol_info and symbol_info.trade_mode == 4
