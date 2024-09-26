import pytest
from unittest.mock import patch
from app import create_app

@pytest.fixture
def client():
    """Sets up the Flask test client and returns it."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@patch('app.redis_client')
def test_get_buoy_data(mock_redis_client, client):
    """Test that /get_buoy_data retrieves data from Redis."""
    mock_redis_client.keys.return_value = ['buoy_data:2024-09-23']
    mock_redis_client.hgetall.return_value = {
        'date': '2024-09-23',
        'time': '10:00',
        'wave_height': '1.5',
        'dpd': '10',
        'direction': '180',
        'temp': '20',
        'estimated_surf_size': '3'
    }

    response = client.get('/get_buoy_data')

    assert response.status_code == 200
    assert b'wave_height' in response.data