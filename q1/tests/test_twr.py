import pytest
import pandas as pd

from q1.twr import calculate_total_time_weighted_return

"""
Please note, floating point comparisons have been done with a tolerance of 1e-9. This number was chosen to reflect a tight tolerance needed in the financial indusrty.
"""

def test_flat_portfolio_returns_zero():
    data = pd.DataFrame({
        "valuation_date": ["01/01/2025", "02/01/2025"],
        "total_valuation" : [1000, 1000],
        "cash_flow": [0, 0]
    })
    result = calculate_total_time_weighted_return(data)
    tol = 1e-9
    mask = result.abs() < tol
    assert mask.all(), f"Found non-zero returns in a dataset which should give zero return: {result[~mask]}"


def test_positive_gain_returns_ten_percent():
    data = pd.DataFrame({
        "valuation_date": ["01/01/2025", "02/01/2025"],
        "total_valuation" : [1000, 1100],
        "cash_flow": [0, 0]
    })
    result = calculate_total_time_weighted_return(data)
    correct_result = [0.0, 0.1]
    assert result.tolist() == pytest.approx(correct_result, rel=1e-9)
    
def test_negative_gain_returns_negative_return():
    data = pd.DataFrame({
        "valuation_date": ["01/01/2025", "02/01/2025"],
        "total_valuation" : [1000, 900],
        "cash_flow": [0, 0]
    })
    result = calculate_total_time_weighted_return(data)
    correct_result = [0.0, -0.1]
    assert result.tolist() == pytest.approx(correct_result, rel=1e-9)

def test_pure_cash_injection_returns_zero():
    data = pd.DataFrame({
        "valuation_date": ["01/01/2025", "02/01/2025"],
        "total_valuation" : [0, 5000],
        "cash_flow": [0, 5000]
    })
    result = calculate_total_time_weighted_return(data)
    correct_result = [0.0, 0.0]
    assert result.tolist() == pytest.approx(correct_result, rel=1e-9)

def test_empty_data_frame_returns_zero():
    data = pd.DataFrame(columns=["valuation_date", "total_valuation", "cash_flow"])
    result = calculate_total_time_weighted_return(data)
    assert result.tolist() == [], "Function incorrectly returns non-zero return for empty data."

def test_multiple_cash_deposit_returns_zero():
    data = pd.DataFrame({
        "valuation_date": ["01/01/2025", "02/01/2025", "03/01/2025"],
        "total_valuation" : [0, 5000, 10000],
        "cash_flow": [0, 5000, 5000]
    })
    result = calculate_total_time_weighted_return(data)
    correct_result = [0.0, 0.0, 0.0]
    assert result.tolist() == pytest.approx(correct_result, rel=1e-9), "Function returns non-zero return for data with only cash injections - should be zero return."

def test_multiple_cash_deposits_with_positive_gain_returns_20_percent():
    data = pd.DataFrame({
        "valuation_date": ["01/01/2025", "02/01/2025", "03/01/2025", "04/01/2025"],
        "total_valuation" : [0, 5500, 11000, 12100],
        "cash_flow": [0, 5000, 5000, 0]
    })
    result = calculate_total_time_weighted_return(data)
    correct_result = [0.0, 0.0, (6000/5500)-1, 0.2]
    assert result.tolist() == pytest.approx(correct_result, rel=1e-9), f"Expected returns of: {correct_result}, but instead got: {result.tolist()}"

def test_single_row_input_returns_zero():
    data = pd.DataFrame({
        "valuation_date": ["01/01/2025"],
        "total_valuation" : [10000],
        "cash_flow": [6000]
    })
    result = calculate_total_time_weighted_return(data)
    correct_result = [0.0]
    assert result.tolist() == pytest.approx(correct_result, rel=1e-9)

def test_pure_cash_withdrawl_returns_zero():
    data = pd.DataFrame({
        "valuation_date": ["01/01/2025", "02/01/2025"],
        "total_valuation" : [10000, 9000],
        "cash_flow": [0, -1000]
    })
    result = calculate_total_time_weighted_return(data)
    correct_result = [0.0, 0.0]
    assert result.tolist() == pytest.approx(correct_result, rel=1e-9)

def test_multiple_withdrawals_then_drop_returns_negative_ten_percent():
    data = pd.DataFrame({
        "valuation_date": ["01/01/2025", "02/01/2025", "03/01/2025", "04/01/2025"],
        "total_valuation" : [10000, 8000, 7200, 6480],
        "cash_flow": [0, -2000, -800, 0]
    })
    result = calculate_total_time_weighted_return(data)
    correct_result = [0.0, 0.0, 0.0, -0.1]
    assert result.tolist() == pytest.approx(correct_result, rel=1e-9)
