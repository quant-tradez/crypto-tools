import argparse
import dataclasses
import datetime
import json
import os
from typing import List, Dict

from binance import Client
from binance.enums import HistoricalKlinesType
from dacite import from_dict

from application.symbol_stats import calculate_symbol_stats
from config import api_key, api_secret
from domain.symbol_stats import SymbolStats
from domain.symbol_stats_dict import SymbolStatsDict
from infrastructure.binance_api_client import get_all_symbols
from util import progressbar


def scan_n_days_ago(
        ticker_suffix: str = "USDT",
        n_days_ago: int = 1,
        kline_type: HistoricalKlinesType = HistoricalKlinesType.FUTURES,
        relative_volume_days: int = 10,
        min_relative_volume: float = 1,
        min_percent_change: float = 0
) -> SymbolStatsDict:
    client = Client(
        api_key=api_key,
        api_secret=api_secret
    )
    symbols: List[str] = get_all_symbols(
        client=client,
        suffix=None if ticker_suffix == '' else ticker_suffix
    )

    stats_datetime = datetime.datetime.today() - datetime.timedelta(days=n_days_ago)
    file_path = os.path.join('cache', '{}_{}_{}_{}_{}.json'.format(
        stats_datetime.date(),
        kline_type,
        ticker_suffix,
        min_relative_volume,
        min_percent_change
    ))
    if os.path.exists(file_path):
        print('{} already exists. loading file...'.format(file_path))
        with open(file_path, mode='r') as file:
            data = json.load(file)
            all_symbol_stats = from_dict(data_class=SymbolStatsDict, data=data)
    else:
        all_symbol_stats: SymbolStatsDict = calculate_all_symbol_stats(
            client=client,
            kline_type=kline_type,
            min_relative_volume=min_relative_volume,
            min_percent_change=min_percent_change,
            n_days_ago=n_days_ago,
            relative_volume_days=relative_volume_days,
            symbols=symbols
        )

    print_stats(all_symbol_stats.stats)
    save_stats_json(file_path, all_symbol_stats.stats)

    return all_symbol_stats


def calculate_all_symbol_stats(
        client: Client,
        kline_type: HistoricalKlinesType,
        min_relative_volume: float,
        min_percent_change: float,
        n_days_ago: int,
        relative_volume_days: int,
        symbols: List[str]
) -> SymbolStatsDict:
    all_symbol_stats: Dict[str, SymbolStats] = {}
    for i in progressbar(range(len(symbols)), "Fetching candles for all tickers: ", 40):
        symbol = symbols[i]
        symbol_stats = calculate_symbol_stats(
            client=client,
            symbol=symbol,
            n_days_ago=n_days_ago,
            relative_volume_days=relative_volume_days,
            min_relative_volume=min_relative_volume,
            min_percent_change=min_percent_change,
            kline_type=kline_type
        )

        if symbol_stats is not None:
            all_symbol_stats[symbol] = symbol_stats

    sorted_symbol_stats = {
        k: v
        for k, v in reversed(sorted(all_symbol_stats.items(), key=lambda item: item[1].percent_change))
    }

    return SymbolStatsDict(sorted_symbol_stats)


def print_stats(sorted_symbol_stats):
    print('\n')
    for k, v in sorted_symbol_stats.items():
        print('{}: {}% RVOL {}'.format(
            k,
            round(v.percent_change * 100, 2),
            round(v.relative_volume, 2)
        ))


def save_stats_json(file_path, sorted_symbol_stats):
    if not os.path.exists('cache'):
        os.mkdir('cache')
    with open(file_path, 'w+') as file:
        json_stats = dataclasses.asdict(SymbolStatsDict(stats=sorted_symbol_stats))
        json.dump(obj=json_stats, fp=file, indent=4)
        print('wrote stats in file: {}'.format(file_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A scanner that sorts crypto by percent changes.')
    parser.add_argument(
        "--n_days_ago",
        help="N days ago (default 1)",
        default=1
    )
    parser.add_argument(
        "--ticker_suffix",
        help="Ticker suffix to filter ticker that end with a currency. (empty by default)",
        default=""
    )

    parser.add_argument(
        "--relative_volume_days",
        help="The amount of days used to calculate relative volume. (default 10)",
        default=10
    )

    parser.add_argument(
        "--min_relative_volume",
        help="Min relative volume for ticker. (default 3)",
        default=3
    )

    parser.add_argument(
        "--min_percent_change",
        help="Min percent change for ticker. (default 0)",
        default=0
    )

    parser.add_argument(
        "--type",
        help="SPOT or FUTURES (default SPOT)",
        default="SPOT"
    )

    args = parser.parse_args()
    print('\n')
    print((datetime.datetime.today() - datetime.timedelta(days=args.n_days_ago)).date())
    print(args)

    scan_n_days_ago(
        n_days_ago=args.n_days_ago,
        ticker_suffix=args.ticker_suffix,
        kline_type=HistoricalKlinesType.FUTURES if args.type == "FUTURES" else HistoricalKlinesType.SPOT,
        relative_volume_days=int(args.relative_volume_days),
        min_relative_volume=float(args.min_relative_volume),
        min_percent_change=float(args.min_percent_change)
    )
