from datetime import datetime
from typing import List, Dict

from binance import Client

from domain.candle import Candle


def get_all_symbols(client: Client, suffix: str = None) -> List[str]:
    symbol_prices: List[Dict[str, str]] = client.get_all_tickers()
    all_symbols: List[str] = []

    for symbol_price in symbol_prices:
        symbol = symbol_price['symbol']
        if suffix is not None:
            if symbol[len(suffix) - 1:] == suffix:
                all_symbols.append(symbol)
        else:
            all_symbols.append(symbol)

    return all_symbols


def get_historical_candles_for_symbol(
        client: Client,
        symbol: str,
        kline_interval: str = Client.KLINE_INTERVAL_1MINUTE,
        start_str: str = "1 day ago UTC"
) -> List[Candle]:
    symbol_klines = client.get_historical_klines(
        symbol=symbol,
        interval=kline_interval,
        start_str=start_str
    )

    candles = []
    for kline in symbol_klines:
        candle = Candle(
            symbol=symbol,
            open_time=datetime.fromtimestamp(int(kline[0]) / 1000),
            open=float(kline[1]),
            high=float(kline[2]),
            low=float(kline[3]),
            close=float(kline[4]),
            volume=float(kline[5]),
            close_time=datetime.fromtimestamp(int(kline[6]) / 1000)
        )
        candles.append(candle)

    return candles
