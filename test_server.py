import pytest
from unittest.mock import patch
from server import app, loadClubs, loadCompetitions


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
    assert response.status_code == 200  
    assert b'Email not found' in response.data

mock_clubs = [
    {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}
]

mock_competitions = [
    {"name": "Spring Festival", "date": "2023-03-27 10:00:00", "numberOfPlaces": "25"},
    {"name": "Powerlifting", "date": "2023-05-20 10:00:00", "numberOfPlaces": "30"}
]

@pytest.fixture(autouse=True)
def mock_data():
    with patch('server.clubs', mock_clubs), \
         patch('server.competitions', mock_competitions):
        yield

def test_book_valid(client):
    response = client.get('/book/Powerlifting/Simply Lift')
    assert response.status_code == 200
    assert b'Booking' in response.data

def test_book_invalid_competition(client):
    response = client.get('/book/Invalid Competition/Simply Lift', follow_redirects=True)
    assert response.status_code == 200
    assert b'Competition not found.' in response.data

def test_book_invalid_club(client):
    response = client.get('/book/Powerlifting/Invalid Club', follow_redirects=True)
    assert response.status_code == 200
    assert b'Club not found.' in response.data

def test_book_missing_parameters(client):
    response = client.get('/book//', follow_redirects=True)
    assert response.status_code == 200
    assert b'Please provide both club and competition names.' in response.data