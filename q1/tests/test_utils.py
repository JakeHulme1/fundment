import pytest
import pandas as pd
import tempfile
import os

from q1.utils import parse_data, validate_csv_filename

class TestValidateCsvFilename:

    def test_filename_has_no_extension_raises_value_error(self):
        filename = "test"
        with pytest.raises(ValueError, match="Invalid file extension"):
            validate_csv_filename(filename)

    def test_filename_contains_extension_not_csv(self):
        filename = "test.xlsx"
        with pytest.raises(ValueError, match="Invalid file extension"):
            validate_csv_filename(filename)

    def test_filename_contains_only_one_csv_extension(self):
        filename = "test.csv.csv"
        with pytest.raises(ValueError, match="Invalid file extension"):
            validate_csv_filename(filename)

    def test_upper_case_csv_extension_passes(self):
        filename = "test.CSV"
        validate_csv_filename(filename)

class TestParseData:

    def test_completely_empty_csv_raises_value_error(self):
        # empty temp file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            with pytest.raises(ValueError, match="completely empty"):
                parse_data(tmp_path)
        finally:
            os.remove(tmp_path) # clean up

    def test_header_only_csv_file_raises_specific_error(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
            tmp.write("valuation_date,total_valuation,cash_flow\n")  # header only
            tmp.flush() # ensure data is saved
            tmp_path = tmp.name
        try:
            with pytest.raises(ValueError, match="column headers but no data"):
                parse_data(tmp_path)
        finally:
            os.remove(tmp_path)

    def test_missing_columns_raises_error(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
            tmp.write("total_valuation,cash_flow\n0, 0")  # missing 'valuation_date' column header
            tmp.flush() # ensure data is saved
            tmp_path = tmp.name
        try:
            with pytest.raises(ValueError, match="Missing required columns"):
                parse_data(tmp_path)
        finally:
            os.remove(tmp_path)

    def test_empty_values_raise_value_error(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
            tmp.write("valuation_date,total_valuation,cash_flow\n01/01/2025,,1000")
            tmp.flush() # ensure data is saved
            tmp_path = tmp.name
        try:
            with pytest.raises(ValueError, match="Missing values"):
                parse_data(tmp_path)
        finally:
            os.remove(tmp_path)

    def test_incorrect_date_format_raises_value_error(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
            tmp.write("valuation_date,total_valuation,cash_flow\n01-01-2025,0,1000")
            tmp.flush() # ensure data is saved
            tmp_path = tmp.name
        try:
            with pytest.raises(ValueError, match="Invalid date format"):
                parse_data(tmp_path)
        finally:
            os.remove(tmp_path)

    def test_non_numeric_entries_raises_value_error(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
            tmp.write("valuation_date,total_valuation,cash_flow\n01/01/2025,a,1000")
            tmp.flush() # ensure data is saved
            tmp_path = tmp.name
        try:
            with pytest.raises(ValueError, match="Non-numeric value found"):
                parse_data(tmp_path)
        finally:
            os.remove(tmp_path)

    def test_file_not_found_raises_error(self):
        file = "non_existent_file.csv"
        with pytest.raises(FileNotFoundError, match="File not found"):
            parse_data(file)

    def test_malformed_csv_raises_parsing_error(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
            tmp.write('valuation_date,total_valuation,cash_flow\n"01/01/2025,1000,1000') # unclosed ""
            tmp.flush() # ensure data is saved
            tmp_path = tmp.name
        try:
            with pytest.raises(ValueError, match="Error parsing CSV file"):
                parse_data(tmp_path)
        finally:
            os.remove(tmp_path)