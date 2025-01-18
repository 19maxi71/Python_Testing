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
"""
Tests for book route
"""

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


"""
Tests for purchasePlaces route
"""

@patch('server.loadClubs', return_value=mock_clubs)
@patch('server.loadCompetitions', return_value=mock_competitions)
def test_purchasePlaces_valid(mock_loadClubs, mock_loadCompetitions, client):
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Powerlifting', 'places': '10'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data

@patch('server.loadClubs', return_value=mock_clubs)
@patch('server.loadCompetitions', return_value=mock_competitions)
def test_purchasePlaces_not_enough_places(mock_loadClubs, mock_loadCompetitions, client):
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Powerlifting', 'places': '31'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Not enough places available' in response.data

@patch('server.loadClubs', return_value=mock_clubs)
@patch('server.loadCompetitions', return_value=mock_competitions)
def test_purchasePlaces_not_enough_points(mock_loadClubs, mock_loadCompetitions, client):
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Powerlifting', 'places': '14'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Not enough points available' in response.data

@patch('server.loadClubs', return_value=mock_clubs)
@patch('server.loadCompetitions', return_value=mock_competitions)
def test_purchasePlaces_too_many_places(mock_loadClubs, mock_loadCompetitions, client):
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Powerlifting', 'places': '13'}, follow_redirects=True)
    assert response.status_code == 200
    # assert b'You can only book up to 12 places per competition' in response.data

@patch('server.loadClubs', return_value=mock_clubs)
@patch('server.loadCompetitions', return_value=mock_competitions)
def test_purchasePlaces_invalid_club(mock_loadClubs, mock_loadCompetitions, client):
    response = client.post('/purchasePlaces', data={'club': 'Invalid Club', 'competition': 'Powerlifting', 'places': '10'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data

@patch('server.loadClubs', return_value=mock_clubs)
@patch('server.loadCompetitions', return_value=mock_competitions)
def test_purchasePlaces_invalid_competition(mock_loadClubs, mock_loadCompetitions, client):
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Invalid Competition', 'places': '10'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data

@patch('server.loadClubs', return_value=mock_clubs)
@patch('server.loadCompetitions', return_value=mock_competitions)
def test_purchasePlaces_missing_parameters(mock_loadClubs, mock_loadCompetitions, client):
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'places': '10'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data
    response = client.post('/purchasePlaces', data={'competition': 'Powerlifting', 'places': '10'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data



"""
Test de Logout
"""
def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/'