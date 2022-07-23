import argparse
import datetime

from binance.enums import HistoricalKlinesType

from scanner import scan_n_days_ago, print_stats

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A scanner that sorts crypto by percent changes.')
    parser.add_argument(
        "--n_days_ago_start",
        help="N days ago start",
        default=1
    )
    parser.add_argument(
        "--n_days_ago_end",
        help="N days ago end",
        default=7
    )
    parser.add_argument(
        "--ticker_suffix",
        help="Ticker suffix to filter ticker that end with a currency.",
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
        help="SPOT or FUTURES",
        default="SPOT"
    )
    args = parser.parse_args()
    print(args)

    symbol_stats_for_all_days = {}
    for i in reversed(list(range(int(args.n_days_ago_start), int(args.n_days_ago_end + 1)))):
        print('\n')
        print((datetime.datetime.today() - datetime.timedelta(days=i)).date())
        print('\n')

        symbol_stats_for_day = scan_n_days_ago(
            n_days_ago=i,
            ticker_suffix=args.ticker_suffix,
            kline_type=HistoricalKlinesType.FUTURES if args.type == "FUTURES" else HistoricalKlinesType.SPOT,
            relative_volume_days=args.relative_volume_days,
            min_relative_volume=float(args.min_relative_volume),
            min_percent_change=float(args.min_percent_change)
        )

        for symbol, stats in symbol_stats_for_day.stats.items():
            symbol_stats_for_all_days[symbol] = stats

    sorted_symbol_stats_all_days = {
        k: v
        for k, v in reversed(sorted(symbol_stats_for_all_days.items(), key=lambda item: item[1].percent_change))
    }

    print('\nFinal list from {} to {}.'.format(
        (datetime.datetime.today() - datetime.timedelta(days=int(args.n_days_ago_start))).date(),
        (datetime.datetime.today() - datetime.timedelta(days=int(args.n_days_ago_end))).date()
    ))
    print_stats(sorted_symbol_stats_all_days)
