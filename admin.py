#-----------------------------------------------------------------------
# admin.py
#-----------------------------------------------------------------------

import flask
import database
import os 
import auth
import dotenv
import random
from flask import Flask, flash, redirect, url_for, request, render_template

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')
dotenv.load_dotenv()
app.secret_key = os.environ['APP_SECRET_KEY']

#-----------------------------------------------------------------------
# GLOBAL VAR DEFAULT VAL FOR ID, NEED TO RESOLVE SECURITY MEASURES
id = 1
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

    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/menu', methods=['GET'])
def menu():
    username = auth.authenticate()
    database.insert_player(username)
    database.insert_player_daily(username)
    
    html_code = flask.render_template('menu.html', username = username)
    # html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/requests', methods=['GET'])
def requests():
    pending_challenges = database.get_user_challenges(auth.authenticate())
    users = database.get_players()
    username = flask.request.args.get('username')

    html_code = flask.render_template('this.html', challenges=pending_challenges, user=auth.authenticate(), users=flask.json.dumps(users), username=username)
    response = flask.make_response(html_code)
    return response

@app.route('/game', methods=['GET'])
def game():

    global id

    username = auth.authenticate()

    # get link from database
    # link = database.query()

    user_played = database.player_played(username)
    today_points = database.get_daily_points(username)
    today_distance = database.get_daily_distance(username)

    if user_played:
        html_code = flask.render_template('alrplayed.html', username = username, today_points = today_points, today_distance = today_distance)
        response = flask.make_response(html_code)
        return response

    print(f"ID WAS {id}")

    if id != database.pic_of_day():
        database.reset_player(username)
        id = database.pic_of_day()
        print(f"ID IS NOW: {id}")

    # coor = database.get_pic_info("coordinates", id)
    link = database.get_pic_info("link", id)

    # get user input using flask.request.args.get('')
    html_code = flask.render_template('gamepage.html', link = link, id = id)
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
    # coor = database.get_distance()
    if not currLat or not currLon:
        return 
    
    # id = flask.request.form.get('id')
    coor = database.get_pic_info("coordinates", id)
    # print(coor)

    distance = database.calc_distance(currLat, currLon, coor)
    username = auth.authenticate()

    today_points = database.calculate_today_points(distance)
    total_points = database.calculate_total_points(username, today_points)
    
    database.update_player(username, total_points)
    database.update_player_daily(username, today_points, distance)
    print("UPDATED")


    html_code = flask.render_template('results.html', dis = distance, lat = currLat, lon = currLon, coor=coor, today_points = today_points)
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
    username = auth.authenticate()
    points = database.get_points(username)
    daily_points = database.get_daily_points(username)
    rank = database.get_rank(username)
    html_code = flask.render_template('leaderboard.html', top_players = top_players, points = points, daily_points = daily_points, rank = rank)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/versus', methods=['GET'])
def versus():
    users = database.get_players()
    username = flask.request.args.get('username')
    html_code = flask.render_template('versus.html', users=flask.json.dumps(users), username=username)
    response = flask.make_response(html_code)
    return response

@app.route('/create-challenge', methods=['POST'])
def create_challenge_route():
    challengee_id = flask.request.form['challengee_id'].strip()  # Trim whitespace
    users = database.get_players()  # Assuming this returns a list of usernames
    
    # Ensure challengee_id is not empty and exists in the users list
    if challengee_id == None or challengee_id not in users or challengee_id == auth.authenticate():
        response = {'status': 'error', 'message': 'Invalid challengee ID'}
        return flask.jsonify(response), 400  # Including a 400 Bad Request status code
    else:
        result = database.create_challenge(auth.authenticate(), challengee_id)
    
    # Handle the response from the database function
    if 'error' in result:
        return flask.jsonify({'status': 'error', 'message': result['error']}), 400  # Consider adding appropriate status codes
    else:
        return flask.jsonify({'status': 'success', 'message': result['success'], 'challenge_id': result['challenge_id']}), 200

@app.route('/accept_challenge', methods=['POST'])
def accept_challenge_route():
    challenge_id = flask.request.form.get('challenge_id')
    result = database.accept_challenge(challenge_id)  # Assuming this returns some result
    if result == "accepted":
        flash('Challenge accepted successfully.')
    else:
        flash('Error accepting challenge.')
    return redirect(url_for('requests'))  # Assuming this is your route name

@app.route('/decline_challenge', methods=['POST'])
def decline_challenge_route():
    challenge_id = flask.request.form.get('challenge_id')
    result = database.decline_challenge(challenge_id)  # Assuming this returns some result
    if result == "declined":
        flash('Challenge declined successfully.')
    else:
        flash('Error declining challenge.')
    return redirect(url_for('requests'))

@app.route('/play_challenge', methods=['POST'])
def play_game():
    challenge_id = flask.request.form.get('challenge_id')
    index = int(flask.request.form.get('index', 0))
    versusList = database.get_random_versus(challenge_id)

    if index < len(versusList):
        link = database.get_pic_info("link", versusList[index])
        html_code = flask.render_template('versusgame.html', challenge_id=challenge_id, index=index, link=link)
        response = flask.make_response(html_code)
        return response
    else:
        html_code = flask.render_template('match.html', challenge_id=challenge_id)
        response = flask.make_response(html_code)
        return response

@app.route('/end_challenge', methods=['POST'])
def end_challenge():
    challenge_id = flask.request.form.get('challenge_id')
    user = auth.authenticate()
    database.update_finish_status(challenge_id, user)
    status = database.check_finish_status(challenge_id)
    if status['status'] == "finished":
        result = database.get_challenge_results(challenge_id)
        database.complete_match(challenge_id, result['winner'], result['challenger_points'], result['challengee_points'])
        return redirect(url_for('requests'))
    else:
        return redirect(url_for('requests'))
    
@app.route('/submit2', methods=['POST'])
def submit2():
    currLat = flask.request.form.get('currLat')  
    currLon = flask.request.form.get('currLon')
    if not currLat or not currLon:
        return 
    index = int(flask.request.form.get('index'))
    challenge_id = flask.request.form.get('challenge_id')
    database.update_versus_pic_status(challenge_id, auth.authenticate(), index+1)
    versusList = database.get_random_versus(challenge_id)
    coor = database.get_pic_info("coordinates", versusList[index])
    distance = database.calc_distance(currLat, currLon, coor)
    points = database.calculate_versus(distance)
    database.store_versus_pic_points(challenge_id, auth.authenticate(), index, points)
    database.update_versus_points(challenge_id, auth.authenticate(), points)
    index = int(index) + 1

    html_code = flask.render_template('versusresults.html', dis = distance, lat = currLat, lon = currLon, coor=coor, index=index, challenge_id=challenge_id, points=points)
    response = flask.make_response(html_code)
    return response
