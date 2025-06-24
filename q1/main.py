import argparse
import pandas as pd

from utils import parse_data
from twr import calculate_total_time_weighted_return

# CLI setup
parser = argparse.ArgumentParser(
    prog='',
    description=''
)
parser.add_argument('input_file', help='Path to the input CSV file')
args = parser.parse_args()

def main():

    # parse data into data frame
    data_frame = parse_data(args.input_file)

    # perform time weighted return calculation
    calculate_total_time_weighted_return(data_frame)

if __name__ =="__main__":
    main()