import os
import flask
import auth
import database
import dotenv

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')
dotenv.load_dotenv()
app.secret_key = os.environ['APP_SECRET_KEY']

#-----------------------------------------------------------------------

# Routes for authentication.

@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return auth.logoutapp()

@app.route('/logoutcas', methods=['GET'])
def logoutcas():
    return auth.logoutcas()

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

    username = auth.authenticate()
    database.insert_or_update_player(username, 0)

    html_code = flask.render_template('index.html', username = username)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/game', methods=['GET'])
def game():
    
    # get link from database
    link = database.query()

    # get user input using flask.request.args.get('')
    #once user clicks submit then get coordinates
    # coor = flask.request.args.get('coordinates')
    html_code = flask.render_template('gamepage.html', link = link)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/rules', methods=['GET'])
def rules():


    html_code = flask.render_template('rules.html')
    response = flask.make_response(html_code)
    return response

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    
    top_players = database.get_top_players()
    html_code = flask.render_template('leaderboard.html', top_players = top_players)
    response = flask.make_response(html_code)
    return response
