import pytest
import pandas as pd
import tempfile
import os
from app.infrastructure.services.csv_user_parser import CsvUserParserService
from app.infrastructure.services.exceptions import CSVParserException
from app.domain.user.models.user import User
from app.domain.user.models.new_user import NewUser

@pytest.fixture
def temp_valid_csv():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        df = pd.DataFrame({
            'id': ['1'],
            'name': ['Test User'],
            'email': ['test@example.com'],
            'age': [25]
        })
        df.to_csv(f.name, index=False)
    yield f.name
    os.unlink(f.name)

@pytest.fixture
def temp_invalid_csv():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        df = pd.DataFrame({
            'name': ['Test User'],
            'email': ['test@example.com'],
            'age': [25]
        })
        df.to_csv(f.name, index=False)
    yield f.name
    os.unlink(f.name)

def test_init_users_valid_csv(temp_valid_csv):
    parser = CsvUserParserService()
    users = parser.init_users(temp_valid_csv)
    
    assert len(users) == 1
    user = users[0]
    assert isinstance(user, User)
    assert user.id == '1'
    assert user.name == 'Test User'
    assert user.email == 'test@example.com'
    assert user.age == 25

def test_init_users_invalid_csv(temp_invalid_csv):
    parser = CsvUserParserService()
    with pytest.raises(CSVParserException):
        parser.init_users(temp_invalid_csv)

def test_load_users_valid_csv(temp_valid_csv):
    parser = CsvUserParserService()
    users = parser.load_users(temp_valid_csv)
    
    assert len(users) == 1
    user = users[0]
    assert isinstance(user, NewUser)
    assert user.name == 'Test User'
    assert user.email == 'test@example.com'
    assert user.age == 25

def test_load_users_invalid_csv(temp_invalid_csv):
    parser = CsvUserParserService()
    with pytest.raises(CSVParserException):
        parser.load_users(temp_invalid_csv) 