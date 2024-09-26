import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test if the index route returns 200 and expected data"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"wave height" in response.data

def test_redis_integration(client, mocker):
    """Test that Redis data fetching works correctly"""
    mock_redis = mocker.patch('app.redis_client')
    mock_redis.get.return_value = b'{"wave_height": 3.5}'
    
    response = client.get('/buoy_data')
    assert response.status_code == 200
    assert b'"wave_height": 3.5' in response.data