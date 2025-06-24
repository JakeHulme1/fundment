import pandas as pd
import os

def validate_csv_filename(file_path: str):
    """
    Throw ValueError when filename extension is not '.csv'.
    """
    filename = os.path.basename(file_path).lower()
    if not filename.endswith('.csv') or filename.count('.csv') != 1:
        raise ValueError(
            f"Invalid file extension. Expected exactly one'.csv', got '{file_path}'. Please rename file extension to '.csv'.")

def parse_data(file_path: str) -> pd.DataFrame:
    """
    Parse .csv data into Pandas DataFrame
    """
    try:
        validate_csv_filename(file_path)
        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError("The input CSV file is empty")
        
        # ensure rquired columns are present
        required_cols = {'total_valuation', 'cash_flow'}
        if not required_cols.issubset(df.columns):
            missing = required_cols - set(df.columns)
            raise ValueError(f"Missing required columns: {', '.join(missing)}")

        # check for any empty values
        if df[["total_valuation", "cash_flow"]].isnull().any().any():
            raise ValueError("Missing values in 'total_valuation' or 'cash_flow' columns")
        
        # ensure all entires in total_valuation and cash_flow columns are numeric
        df["total_valuation"] = pd.to_numeric(df["total_valuation"], errors="raise")
        df["cash_flow"] = pd.to_numeric(df["cash_flow"], errors="raise")

        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except pd.errors.ParserError as e:
        raise RuntimeError(f"Error parsing CSV file: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the file: {e}")
