from typing import List, Optional

from binance import Client
from binance.enums import HistoricalKlinesType

from domain.candle import Candle
from domain.symbol_stats import SymbolStats
from infrastructure.binance_api_client import get_historical_candles_for_symbol


def calculate_symbol_stats(
    client: Client,
    symbol: str,
    n_days_ago: int,
    relative_volume_days: int,
    min_relative_volume: float,
    min_percent_change: float,
    kline_type: HistoricalKlinesType
) -> Optional[SymbolStats]:
    start_str = "{} days ago UTC".format(n_days_ago + relative_volume_days)
    candles: List[Candle] = get_historical_candles_for_symbol(
        client=client,
        symbol=symbol,
        kline_interval=Client.KLINE_INTERVAL_1DAY,
        kline_type=kline_type,
        start_str=start_str,
    )
    if candles is None:
        return None

    if candles is None or len(candles) < relative_volume_days:
        return None

    if len(candles) - 1 < relative_volume_days:
        return None

    stats_day_candle = candles[relative_volume_days]
    average_volume = sum([c.volume for c in candles[0:relative_volume_days]]) / len(candles)
    if stats_day_candle.volume == 0 or average_volume == 0:
        return None

    relative_volume = stats_day_candle.volume / average_volume
    if min_relative_volume != 0 and relative_volume < min_relative_volume:
        return None

    percent_change = (stats_day_candle.close - stats_day_candle.open) / stats_day_candle.open

    if min_percent_change != 0 and percent_change < min_percent_change:
        return None

    return SymbolStats(
        symbol=symbol,
        percent_change=percent_change,
        relative_volume=relative_volume
    )

