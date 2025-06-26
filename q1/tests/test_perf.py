import time
import numpy as np
import pandas as pd

from q1.twr import calculate_total_time_weighted_return

def random_valuation_df(size: int) -> pd.Series:
    """Helper function to create a random pd.Series of specified length"""

    dates = pd.date_range("2025-01-01", periods=size, freq="D")
    np.random.seed(42)
    valuations = 1000 + np.cumsum(np.random.rand(size))
    cash_flows = np.random.choice([0.0, 50.0, -50.0], size=size, p=[0.8, 0.1, 0.1])
    return pd.DataFrame({
        "valuation_date": dates.strftime("%d/%m/%Y"),  # matches sample_valuations.csv date column
        "total_valuation": valuations,
        "cash_flow": cash_flows,
    })

def test_twr_performance_on_large_input():
    n = 1000
    df = random_valuation_df(n)

    # measure execution time
    start = time.perf_counter()
    result = calculate_total_time_weighted_return(df)
    elapsed = time.perf_counter() - start

    assert len(result) == n

    # decided a reasonable time was under 0.1s
    assert elapsed < 0.1, f"Time weighted return too slow: {elapsed:.2f}s for {n} rows"

def test_scalability_of_twr_algorithm():
    n1 = 1000
    n2 = 10000

    df1 = random_valuation_df(n1)
    df2 = random_valuation_df(n2)

    # measure execution time
    start1 = time.perf_counter()
    result1 = calculate_total_time_weighted_return(df1)
    elapsed1 = time.perf_counter() - start1

    start2 = time.perf_counter()
    result2 = calculate_total_time_weighted_return(df2)
    elapsed2 = time.perf_counter() - start2


    # given headroom of 20% to allow for noise
    assert elapsed2 < 10 * elapsed1 * 1.2
