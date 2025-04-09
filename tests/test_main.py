from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_app_exception_handler():
    """測試自定義異常處理器"""
    from app.core.exceptions import AppBaseException
    
    class TestException(AppBaseException):
        def __init__(self):
            self.status_code = 400
            self.detail = "Test error message"
            self.exception_type = "TEST_ERROR"
    
    @app.get("/test-exception")
    def raise_test_exception():
        raise TestException()
    
    response = client.get("/test-exception")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "TEST_ERROR: Test error message"
    } 