import time
import numpy as np
import pandas as pd
import pytest

from q1.twr import calculate_total_time_weighted_return

def test_twr_performance_on_large_input():
    n = 1000
    dates = pd.date_range("2025-01-01", periods=n, freq="D")

    np.random.seed(42)
    valuations = 1000 + np.cumsum(np.random.randn(n))
    cash_flows = np.random.choice([0.0, 50.0, -50.0], size=n, p=[0.9, 0.05, 0.05])

    df = pd.DataFrame({
        "valuation_date": dates.strftime("%d/%m/%Y"),
        "total_valuation": valuations,
        "cash_flow": cash_flows,
    })

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
    dates1 = pd.date_range("2025-01-01", periods=n1, freq="D")
    dates2 = pd.date_range("2025-01-01", periods=n2, freq="D")

    np.random.seed(42)
    valuations1 = 1000 + np.cumsum(np.random.randn(n1))
    cash_flows1 = np.random.choice([0.0, 50.0, -50.0], size=n1, p=[0.9, 0.05, 0.05])
    valuations2 = 1000 + np.cumsum(np.random.randn(n2))
    cash_flows2 = np.random.choice([0.0, 50.0, -50.0], size=n2, p=[0.9, 0.05, 0.05])

    df1 = pd.DataFrame({
        "valuation_date": dates1.strftime("%d/%m/%Y"),
        "total_valuation": valuations1,
        "cash_flow": cash_flows1,
    })
    df2 = pd.DataFrame({
        "valuation_date": dates2.strftime("%d/%m/%Y"),
        "total_valuation": valuations2,
        "cash_flow": cash_flows2
    })

    # measure execution time
    start1 = time.perf_counter()
    result1 = calculate_total_time_weighted_return(df1)
    elapsed1 = time.perf_counter() - start1

    start2 = time.perf_counter()
    result2 = calculate_total_time_weighted_return(df2)
    elapsed2 = time.perf_counter() - start2


    # given headroom of 20% to allow for noise
    assert elapsed2 < 10 * elapsed1 * 1.2
