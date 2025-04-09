from fastapi.testclient import TestClient
from app.main import app
from app.core.exceptions import AppBaseException

client = TestClient(app)

def test_app_exception_handler(client, test_app):
    """測試自定義異常處理器"""
    class TestException(AppBaseException):
        status_code = 400
        detail = "Test error message"
        exception_type = "TEST_ERROR"
    
    @test_app.get("/test-exception")
    def raise_test_exception():
        raise TestException()
    
    response = client.get("/test-exception")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "TEST_ERROR: Test error message"
    } 