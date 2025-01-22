import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

"""
Déclare the INDEX_ROUTE constante et assigne la valeur 'index' à cette constante 
pour définir la route de la page d'accueil.
"""
INDEX_ROUTE = 'index'
CLUBS_POINTS_ROUTE = 'clubsPoints'


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
    except IndexError:
        flash('Email not found')
        return redirect(url_for(INDEX_ROUTE))
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/', defaults={'competition': None, 'club': None})
@app.route('/book/<competition>/', defaults={'club': None})
@app.route('/book/<competition>/<club>')
def book(competition, club):
    if not competition or not club:
        flash('Please provide both club and competition names.')
        return redirect(url_for(INDEX_ROUTE))

    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)
    
    if not foundClub:
        flash('Club not found.')
    elif not foundCompetition:
        flash('Competition not found.')
    elif foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    
    return redirect(url_for(INDEX_ROUTE))


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = next((c for c in competitions if c['name'] == request.form.get('competition')), None)
    club = next((c for c in clubs if c['name'] == request.form.get('club')), None)
    placesRequired = request.form.get('places')
    
    if not competition or not club or not placesRequired:
        flash("Something went wrong-please try again")
        return redirect(url_for(INDEX_ROUTE))
    
    placesRequired = int(placesRequired)
    clubPoints = int(club['points'])
    availablePlaces = int(competition['numberOfPlaces'])
    
    if placesRequired > availablePlaces:
        flash('Not enough places available')
    elif placesRequired > clubPoints:
        flash('Not enough points available')
    elif placesRequired > 12:
        flash('You can only book up to 12 places per competition')
        print("Flash message set: You can only book up to 12 places per competition")
    else:
        competition['numberOfPlaces'] = availablePlaces - placesRequired
        club['points'] = clubPoints - placesRequired
        flash('Great-booking complete!')
    
    return render_template('welcome.html', club=club, competitions=competitions)



# TODO: Add route for points display
@app.route('/clubsPoints')
def clubsPoints():
    return render_template('clubsPoints.html', clubs=clubs, competitions=competitions)




@app.route('/logout')
def logout():
    return redirect(url_for(INDEX_ROUTE))