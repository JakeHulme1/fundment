"""
CSV parsing and validation utilities for valuation data.

- validate_csv_filename: guard against bad file extensions
- parse_data: load CSV and enforce table layout, types and formats
"""

import os
import pandas as pd

# HELPER FUNCTIONS

def ensure_required_columns(df: pd.DataFrame, required: set[str]) -> None:
    """Raise if any of the required columns are missing."""
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    
def ensure_no_nulls(df: pd.DataFrame, columns: list[str]) -> None:
    """Raise if any of the given colums contain null values."""
    if df[columns].isna().any().any():
        raise ValueError(f"Missing values in required columns: {', '.join(columns)}")
    
def ensure_numeric_colum(df: pd.DataFrame, column:str) -> None:
    """Raise if any of the given columns contain non-numeric values"""
    try:
        df[column] = pd.to_numeric(df[column], errors="raise")
    except ValueError:
        raise ValueError(f"Non-numeric value found in '{column}' column")
    
def ensure_date_format_column(df: pd.DataFrame, column: str, format: str):
    """Raise if any of the given columns contain a format other than the specified argument 'format'."""
    try:
        df[column] = pd.to_datetime(df[column], format=format)
    except ValueError:
        raise ValueError(f"Invalid date format in '{column}'. Expected format: {format}")
    
# VALIDATION FUNCTION

def validate_csv_filename(file_path: str) -> None:
    """Raise if the CSV filename is bad."""
    filename = os.path.basename(file_path).lower()
    if not filename.endswith('.csv') or filename.count('.csv') != 1:
        raise ValueError(
            f"Invalid file extension. Expected exactly one'.csv', got '{file_path}'. Please rename file extension to '.csv'.")

# DATA PARSING FUNCTION

def parse_data(file_path: str) -> pd.DataFrame:
    """Load and validate a CSV of valuations. Raises ValueError or FileNotFOund error for I/O errors, structural errors, and field specific errors. """
    # load file, catch I/O errors and parser errors
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except pd.errors.EmptyDataError:
        raise ValueError("CSV file is completely empty")
    except pd.errors.ParserError as e:
        raise ValueError(f"Error parsing CSV file: {e}")
    
    # header-only check
    if df.empty:
        raise ValueError("The CSV file has column headers but no data")
    
    required_cols = {"valuation_date", "total_valuation", "cash_flow"}
    ensure_required_columns(df, required_cols)
     # use list for ordered column selection in pandas indexing
    ensure_no_nulls(df, list(required_cols))

    # field specific validations
    ensure_date_format_column(df, "valuation_date", "%d/%m/%Y")
    ensure_numeric_colum(df, "total_valuation")
    ensure_numeric_colum(df, "cash_flow")

    # sort by date for downstream code
    df = df.sort_values("valuation_date").reset_index(drop=True)
    return df