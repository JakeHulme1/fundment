import argparse
import pandas as pd

from utils import validate_csv_filename, parse_data

# CLI setup
parser = argparse.ArgumentParser(
    prog='',
    description=''
)
parser.add_argument('input_file', help='Path to the input CSV file')
args = parser.parse_args()

def main():

    # validate the filename
    validate_csv_filename(args.input_file)

    # parse data into data frame
    data_frame = parse_data(args.input_file)

    # perform time weighted return calculation
    calculate_total_time_weighted_return(data_frame)

if __name__ =="__main__":
    main()