import pandas as pd
import pytest
import os
from src.data_validation import validate_payments_data
from src.logger import setup_logger

# Configure the logger for tests (optional, to see logs during test)
logger = setup_logger()

# Mock OUTPUT_DIR to avoid real writing during tests
@pytest.fixture(autouse=True)
def mock_output_dir(monkeypatch):
    monkeypatch.setattr('src.config.OUTPUT_DIR', './test_output')
    # Ensure the test directory is cleaned before each test
    if os.path.exists('./test_output'):
        import shutil
        shutil.rmtree('./test_output')
    os.makedirs('./test_output', exist_ok=True)

def test_valid_data():
    data = {
        'ssn': ['111', '222'],
        'payment_date': ['2023-01-01', '2023-02-01'],
        'amount': [100.0, 200.0],
        'beneficiary_name': ['John', 'Jane']
    }
    df = pd.DataFrame(data)
    assert validate_payments_data(df, logger) == True

def test_missing_column():
    data = {
        'ssn': ['111'],
        'payment_date': ['2023-01-01'],
        'amount': [100.0]
    }
    df = pd.DataFrame(data)
    assert validate_payments_data(df, logger) == False

def test_null_amount():
    data = {
        'ssn': ['111'],
        'payment_date': ['2023-01-01'],
        'amount': [None],
        'beneficiary_name': ['John']
    }
    df = pd.DataFrame(data)
    assert validate_payments_data(df, logger) == False

def test_negative_amount():
    data = {
        'ssn': ['111'],
        'payment_date': ['2023-01-01'],
        'amount': [-100.0],
        'beneficiary_name': ['John']
    }
    df = pd.DataFrame(data)
    assert validate_payments_data(df, logger) == False

def test_invalid_date_format():
    data = {
        'ssn': ['111'],
        'payment_date': ['invalid-date'],
        'amount': [100.0],
        'beneficiary_name': ['John']
    }
    df = pd.DataFrame(data)
    assert validate_payments_data(df, logger) == False
