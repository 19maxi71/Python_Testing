import pytest
from server import app, clubs, competitions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_showSummary_valid_email(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_showSummary_invalid_email(client):
    response = client.post('/showSummary', data={'email': 'invalid@example.com'}, follow_redirects=True)
    assert response.status_code == 200  # Should be 200 after following the redirect
    assert b'Email not found' in response.data