import pandas as pd
import numpy as np

def calculate_total_time_weighted_return(data: pd.DataFrame) -> pd.Series:
    """
    Returns the decimal proportion of the total time weighted return.
    """
    prev_valuation = 0
    weighted_returns = []
    for row in data.itertuples(index=False): # (itertuples() significantly faster than iterrows())

        if prev_valuation == 0:
            # initilise and skip first loop
            prev_valuation = row.total_valuation
            continue
        
        if row.total_valuation + row.cash_flow == 0:
            # no change in return so continue
            continue
        
        # calculate return for sub period
        sub_return = (row.total_valuation - row.cash_flow) / prev_valuation

        # append to list 
        weighted_returns.append(sub_return)

        # update the previous total_valuation for next loop
        prev_valuation = row.total_valuation
    
    # calculate total time weighted return
    # (numpy.prod() much faster than a for loop as it uses C)
    twr = np.prod(weighted_returns) - 1

    print("weighted_returns = ")
    print(weighted_returns)
    print(pd.Series([twr]))

    return pd.Series([twr])