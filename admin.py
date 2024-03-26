import flask
import database

app = flask.Flask(__name__, template_folder='.')

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response


@app.route('/game', methods=['GET'])
def game():
    # get link from database
    link = database.query()
    html_code = flask.render_template('gamepage.html', link = link)
    response = flask.make_response(html_code)
    return response

@app.route('/submit', methods=['GET'])
def submit():
    # get user input using flask.request.args.get('')
    #once user clicks submit then get coordinates 
    currLat = flask.request.form['currLat']
    currLon = flask.request.form['currLon']


    html_code = flask.render_template('submit.html', lat = currLat, lon = currLon )
    response = flask.make_response(html_code)
    return response


@app.route('/rules', methods=['GET'])
def rules():
    html_code = flask.render_template('rules.html')
    response = flask.make_response(html_code)
    return response

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    html_code = flask.render_template('leaderboard.html')
    response = flask.make_response(html_code)
    return response

