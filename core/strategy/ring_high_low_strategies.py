from core.strategy.base import Strategy


class RingLowStrategy(Strategy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.caption = "Potential Ring-Low pattern"
        self.callback_code = "rl"


class RingHighStrategy(Strategy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.caption = "Potential Ring-High pattern"
        self.callback_code = "rh"
