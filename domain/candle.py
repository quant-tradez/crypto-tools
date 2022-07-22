import datetime
from dataclasses import dataclass


@dataclass
class Candle:
    symbol: str
    open: float
    open_time: datetime.datetime
    close: float
    close_time: datetime.datetime
    low: float
    high: float
    volume: float
