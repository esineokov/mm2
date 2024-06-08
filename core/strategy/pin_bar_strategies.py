from core.strategy.base import Strategy


class BullishPinBarStrategy(Strategy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.caption = "Potential Bullish Pin Bar"
        self.code = "uppb"


class BearishPinBarStrategy(Strategy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.caption = "Potential Bearish Pin Bar"
        self.callback_code = "downpb"
