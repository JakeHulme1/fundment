import os
import pandas as pd

def validate_csv_filename(file_path: str):
    """
    Throw ValueError when filename extension is not '.csv'.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if not file_path.lower().endswith('.csv') or file_path.lower().count('.csv') != 1:
        raise ValueError(
            f"Invalid file extension. Expected exactly one'.csv', got '{file_path}'. Please rename file extension to '.csv'.")

def parse_data(file_path: str) -> pd.DataFrame:
    """
    Parse .csv data into Pandas DataFrame
    """
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            raise ValueError("The input CSV file is empty")
        
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"An error occured while reading the file: {e}")