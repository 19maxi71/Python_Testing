import pytest
from server import app
from unittest.mock import patch

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

# Mock data
mock_clubs = [
    {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}
]

mock_competitions = [
    {"name": "Spring Festival", "date": "2023-03-27 10:00:00", "numberOfPlaces": "25"},
    {"name": "Powerlifting", "date": "2023-05-20 10:00:00", "numberOfPlaces": "30"}
]

@patch('server.loadClubs', return_value=mock_clubs)
@patch('server.loadCompetitions', return_value=mock_competitions)
def test_book_valid(client, mock_loadClubs, mock_loadCompetitions):
    response = client.get('/book/Powerlifting/SimplyLift')
    assert response.status_code == 200
    assert b'Booking' in response.data

@patch('server.loadClubs', return_value=mock_clubs)
@patch('server.loadCompetitions', return_value=mock_competitions)
def test_book_invalid(client, mock_loadClubs, mock_loadCompetitions):
    response = client.get('/book/Powerlifting/InvalidClub')
    assert response.status_code == 200
    assert b'Something went wrong-please try again' in response.data