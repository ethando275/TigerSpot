#-----------------------------------------------------------------------
# admin.py
#-----------------------------------------------------------------------

import flask
import database
import os 
import auth
import dotenv

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')
dotenv.load_dotenv()
app.secret_key = os.environ['APP_SECRET_KEY']

#-----------------------------------------------------------------------



@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    username = auth.authenticate()
    database.insert_player(username, 0)
    
    html_code = flask.render_template('index.html', username = username)
    # html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------


@app.route('/game', methods=['GET'])
def game():
    # get link from database
    link = database.query()
    # get user input using flask.request.args.get('')
    html_code = flask.render_template('gamepage.html', link = link)
    response = flask.make_response(html_code)
    # distance = flask.request.args.get('distance')
    # print('Distance: ' + distance)
    return response

#-----------------------------------------------------------------------

@app.route('/submit', methods=['POST'])
def submit():
    # get user input using flask.request.args.get('')
    #once user clicks submit then get coordinates 
    currLat = flask.request.form.get('currLat')  # Use .get for safe retrieval
    # print(currLat)
    currLon = flask.request.form.get('currLon')
    # print(currLon)
    coor = database.get_distance()
    # print(coor)

    distance = database.calc_distance(currLat, currLon, coor)
    username = auth.authenticate()

    points = database.calculate_points(username, distance)
    database.update_player(username, points)

    html_code = flask.render_template('results.html', dis = distance, lat = currLat, lon = currLon)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/rules', methods=['GET'])
def rules():
    html_code = flask.render_template('rules.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    top_players = database.get_top_players()
    html_code = flask.render_template('leaderboard.html', top_players = top_players)
    response = flask.make_response(html_code)
    return response