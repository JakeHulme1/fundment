import sys
import argparse
import pandas as pd

from utils import parse_data
from twr import calculate_total_time_weighted_return

def parse_args():
    parser = argparse.ArgumentParser(
        prog="total time weighted return calculator",
        description="Compute the time-weighted return for a valuation CSV."
    )
    parser.add_argument(
        "input_file",
        help="Path to the CSV file with columns: valuation_date, total_valuation, cash_flow"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    try:
        df = parse_data(args.input_file)
        twr_series = calculate_total_time_weighted_return(df)
        print(twr_series)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)


if __name__ =="__main__":
    main()