import pandas as pd
import numpy as np

def calculate_total_time_weighted_return(data: pd.DataFrame) -> pd.Series:
    """
    Returns the decimal proportion of the total time weighted return.

    Args:
        - data (pandas.DataFrame) - this must contain the columns 'total_valuation' and 'cash_flow' and be sorted by date.

    Returns:
        - a pandas.Series containing the total weighted return indexed with each sub-period.
    """
    dates = []
    twr_values = []
    running_factor = 1.0
    prev_val = None

    for row in data.itertuples(index=False): # (itertuples() significantly faster than iterrows())

        date = pd.to_datetime(row.valuation_date, format="%d/%m/%Y")
        dates.append(date)
        current_val = row.total_valuation
        cash_flow = row.cash_flow

        if prev_val == None: # first iteration set the return as 0 as a convention
            twr_values.append(0.0)
            prev_val = current_val
            continue
        
        if prev_val != 0:
            factor = (current_val - cash_flow) / prev_val
        else: # avoids division by zero
            factor = 1.0

        running_factor *= factor
        twr_values.append(running_factor - 1)
    
        prev_val = current_val

    return pd.Series(data=twr_values, 
                     index=pd.DatetimeIndex(dates),
                     name='time_weighted_return')