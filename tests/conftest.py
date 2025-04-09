import pytest
from fastapi.testclient import TestClient
from app.main import app
import os
import sys

# 添加項目根目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def client():
    """創建測試客戶端"""
    return TestClient(app)

@pytest.fixture
def test_app():
    """返回應用實例"""
    return app 