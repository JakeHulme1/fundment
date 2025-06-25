import pytest
import pandas as pd

from q1.twr import calculate_total_time_weighted_return

"""
Please note, floating point comparisons have been done with a relativity of 1e-9. This number was chosen to reflect a tight tolerance needed in the financial indusrty.
"""

def test_flat_portfolio_returns_zero():
    data = pd.DataFrame({
        "valuation_date": ["01/01/2025", "02/01/2025"],
        "total_valuation" : [1000, 1000],
        "cash_flow": [0, 0]
    })
    result = calculate_total_time_weighted_return(data)
    assert result.item() == pytest.approx(0.0, rel=1e-9), "Flat portfolio did not return zero." # use pytest.approx() to mitigate any floating point maths errors

def test_positive_gain_returns_positive_return():
    data = pd.DataFrame({
        "valuation_date": ["01/01/2025", "02/01/2025"],
        "total_valuation" : [1000, 1100],
        "cash_flow": [0, 0]
    })
    result = calculate_total_time_weighted_return(data)
    assert result.item() == pytest.approx(0.1, rel=1e-9), "Data which showcases a positive gain of 0.1 did not return 0.1."

def test_negative_gain_returns_negative_return():
    data = pd.DataFrame({
        "valuation_date": ["01/01/2025", "02/01/2025"],
        "total_valuation" : [1000, 900],
        "cash_flow": [0, 0]
    })
    result = calculate_total_time_weighted_return(data)
    assert result.item() == pytest.approx(-0.1, rel=1e-9), "Data which showcases a negative gain of 0.1 did not return -0.1."

def test_pure_cash_injection_returns_zero():
    data = pd.DataFrame({
        "valuation_date": ["01/01/2025", "02/01/2025"],
        "total_valuation" : [0, 5000],
        "cash_flow": [0, 5000]
    })
    result = calculate_total_time_weighted_return(data)
    assert result.item() == pytest.approx(0.0, rel=1e-9), "Data which exhibits a pure cash injection, which means no return, actaully resulted in a positive or negative return."

def test_empty_data_frame_returns_zero():
    data = pd.DataFrame(columns=["valuation_date", "total_valuation", "cash_flow"])
    result = calculate_total_time_weighted_return(data)
    assert result.item() == pytest.approx(0.0, rel=1e-9), "Function returns non-zero return for empty data."

def test_multiple_cash_deposit_returns_zero():
    data = pd.DataFrame({
        "valuation_date": ["01/01/2025", "02/01/2025", "03/01/2025"],
        "total_valuation" : [0, 5000, 10000],
        "cash_flow": [0, 5000, 5000]
    })
    result = calculate_total_time_weighted_return(data)
    assert result.item() == pytest.approx(0.0, rel=1e-9), "Function returns non-zero return for data with only cash injections - should be zero return."

def test_multiple_cash_deposits_with_positive_gain_returns_20_percent():
    data = pd.DataFrame({
        "valuation_date": ["01/01/2025", "02/01/2025", "03/01/2025", "04/01/2025"],
        "total_valuation" : [0, 5500, 11000, 12100],
        "cash_flow": [0, 5000, 5000, 0]
    })
    result = calculate_total_time_weighted_return(data)
    assert result.item() == pytest.approx(0.2, rel=1e-9)