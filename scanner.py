from typing import List
import argparse

from binance import Client

from domain.candle import Candle
from infrastructure.binance_api_client import get_all_symbols, get_historical_candles_for_symbol
from config import api_key, api_secret
from util import progressbar


def main(ticker_suffix: str, start_str: str):
    client = Client(
        api_key=api_key,
        api_secret=api_secret
    )
    symbols: List[str] = get_all_symbols(
        client=client,
        suffix=None if ticker_suffix == '' else ticker_suffix
    )
    print('python scanner.py --ticker_suffix: \'{}\' --start_str: \'{}\'\n'.format(ticker_suffix, start_str))

    open_time = ''
    symbol_percent_change = {}
    for i in progressbar(range(len(symbols)), "Fetching candles for all tickers: ", 40):
        symbol = symbols[i]
        candles: List[Candle] = get_historical_candles_for_symbol(
            client=client,
            symbol=symbol,
            kline_interval=Client.KLINE_INTERVAL_1DAY,
            start_str=start_str
        )
        if len(candles) > 0:
            open_time = candles[0].open_time
            symbol_percent_change[symbol] = (candles[0].close - candles[0].open) / candles[0].open

    sorted_symbol_percent_change = {
        k: v
        for k, v in reversed(sorted(symbol_percent_change.items(), key=lambda item: item[1]))
    }

    print(open_time)
    print('\n')
    for k, v in sorted_symbol_percent_change.items():
        print('{}: {}%'.format(k, round(v * 100, 2)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A scanner that sorts crypto by percent changes.')
    parser.add_argument(
        "--start_str",
        help="Start date string in utc format or timestamp in milliseconds.",
        default="2 days ago UTC"
    )
    parser.add_argument(
        "--ticker_suffix",
        help="Ticker suffix to filter ticker that end with a currency.",
        default=""
    )

    args = parser.parse_args()

    main(
        start_str=args.start_str,
        ticker_suffix=args.ticker_suffix
    )
