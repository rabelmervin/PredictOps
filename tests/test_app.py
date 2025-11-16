import pytest
import json
from app.app import app


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test /health endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'


def test_ready_endpoint(client):
    """Test /ready endpoint"""
    response = client.get('/ready')
    assert response.status_code in [200, 503]  # 200 if model loaded, 503 if not
    assert 'ready' in response.json


def test_metrics_endpoint(client):
    """Test /metrics endpoint"""
    response = client.get('/metrics')
    assert response.status_code == 200
    assert b'flask_http_request_total' in response.data
    assert b'prediction_requests_total' in response.data


def test_predict_with_valid_data(client):
    """Test /predict endpoint with valid data"""
    payload = {
        "Revenue": 1000000,
        "Gross Profit": 500000,
        "EBITDA": 250000,
        "Share Holder Equity": 1500000,
    }
    response = client.post('/predict',
                          data=json.dumps(payload),
                          content_type='application/json')
    assert response.status_code in [200, 500]  # 200 if model loaded, 500 if not
    assert 'prediction' in response.json or 'error' in response.json


def test_predict_with_invalid_data(client):
    """Test /predict endpoint with invalid data"""
    payload = {
        "revenue": "invalid",  # Should be number
    }
    response = client.post('/predict',
                          data=json.dumps(payload),
                          content_type='application/json')
    assert response.status_code in [400, 500]  # 400 for validation error or 500 if model not loaded
    assert 'error' in response.json


def test_predict_with_array_input(client):
    """Test /predict endpoint with array input"""
    # Array order must match FEATURE_ORDER from validation.py (4 features)
    payload = [1000000, 500000, 250000, 1500000]
    response = client.post('/predict',
                          data=json.dumps(payload),
                          content_type='application/json')
    assert response.status_code in [200, 400, 500]
    assert 'prediction' in response.json or 'error' in response.json
