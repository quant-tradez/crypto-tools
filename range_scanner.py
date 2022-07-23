import argparse
import datetime

from binance.enums import HistoricalKlinesType

from scanner import scan_n_days_ago

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

    for i in range(int(args.n_days_ago_start), int(args.n_days_ago_end + 1)):
        print('\n')
        print((datetime.datetime.today() - datetime.timedelta(days=i)).date())
        print('\n')

        scan_n_days_ago(
            n_days_ago=i,
            ticker_suffix=args.ticker_suffix,
            kline_type=HistoricalKlinesType.FUTURES if args.type == "FUTURES" else HistoricalKlinesType.SPOT,
            relative_volume_days=args.relative_volume_days,
            min_relative_volume=float(args.min_relative_volume),
            min_percent_change=float(args.min_percent_change)
        )
