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
