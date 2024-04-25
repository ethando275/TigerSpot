#-----------------------------------------------------------------------
# admin.py
#-----------------------------------------------------------------------

import flask
import database
import challenges_database
import matches_database
import versus_database
import pictures_database
import user_database
import os 
import auth
import dotenv
import distance_func
import daily_user_database
import points
import user_database
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

@app.route('/sam', methods=['GET'])
def sam():
    html_code = flask.render_template('sam.html')
    response = flask.make_response(html_code)
    return response

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
    user_database.insert_player(username)
    daily_user_database.insert_player_daily(username)
    
    html_code = flask.render_template('menu.html', username = username)
    # html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/requests', methods=['GET'])
def requests():
    pending_challenges = challenges_database.get_user_challenges(auth.authenticate())
    users = user_database.get_players()
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

    user_played = daily_user_database.player_played(username)
    today_points = daily_user_database.get_daily_points(username)
    today_distance = daily_user_database.get_daily_distance(username)

    print(f"ID WAS: {id}")

    played_date = daily_user_database.get_last_played_date(username)
    print(f"LAST PLAYED DATE WAS: {played_date}")

    current_date = pictures_database.get_current_date()
    print(f"CURRENT DATE IS: {current_date}")

    if  played_date != current_date:
        daily_user_database.reset_player(username)
        user_played = daily_user_database.player_played(username)
        challenges_database.clear_challenges_table()
        challenges_database.reset_challenges_id_sequence()
        matches_database.clear_matches_table()
        id = pictures_database.pic_of_day()
        print(f"RESET ID IS NOW: {id}")

    if user_played:
        html_code = flask.render_template('alrplayed.html', username = username, today_points = today_points, today_distance = today_distance)
        response = flask.make_response(html_code)
        return response

    print(f"CURRENT ID IS {id}")

    # coor = database.get_pic_info("coordinates", id)
    link = pictures_database.get_pic_info("link", id)

    # get user input using flask.request.args.get('')
    html_code = flask.render_template('gamepage.html', link = link, id = id)
    response = flask.make_response(html_code)
    # distance = flask.request.args.get('distance')
    # print('Distance: ' + distance)
    return response


#-----------------------------------------------------------------------

@app.route('/submit', methods=['POST'])
def submit():

    username = auth.authenticate()

    user_played = daily_user_database.player_played(username)
    today_points = daily_user_database.get_daily_points(username)
    today_distance = daily_user_database.get_daily_distance(username)

    print(f"INSIDE SUBMIT: user played is {user_played}")

    if user_played:
        html_code = flask.render_template('alrplayed.html', username = username, today_points = today_points, today_distance = today_distance)
        response = flask.make_response(html_code)
        return response

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
    coor = pictures_database.get_pic_info("coordinates", id)
    place = pictures_database.get_pic_info("place", id)
    # print(coor)

    distance = distance_func.calc_distance(currLat, currLon, coor)
    username = auth.authenticate()

    today_points = points.calculate_today_points(distance)
    total_points = points.calculate_total_points(username, today_points)
    
    user_database.update_player(username, total_points)
    daily_user_database.update_player_daily(username, today_points, distance)
    print("UPDATED")

    html_code = flask.render_template('results.html', dis = distance, lat = currLat, lon = currLon, coor=coor, today_points = today_points, place = place, today_distance = distance)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/rules', methods=['GET'])
def rules():
    html_code = flask.render_template('rules.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/team', methods=['GET'])
def team():
    html_code = flask.render_template('team.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/totalboard', methods=['GET'])
def leaderboard():
    top_players = user_database.get_top_players()
    username = auth.authenticate()
    points = user_database.get_points(username)
    daily_points = daily_user_database.get_daily_points(username)
    rank = user_database.get_rank(username)
    daily_rank = daily_user_database.get_daily_rank(username)
    streak = daily_user_database.get_streak(username)
    html_code = flask.render_template('totalboard.html', top_players = top_players, points = points, daily_points = daily_points, rank = rank, daily_rank = daily_rank, streak = streak)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/leaderboard', methods=['GET'])   
def totalleaderboard():
    top_players = daily_user_database.get_daily_top_players()
    username = auth.authenticate()
    points = user_database.get_points(username)
    daily_points = daily_user_database.get_daily_points(username)
    rank = user_database.get_rank(username)
    daily_rank = daily_user_database.get_daily_rank(username)
    streak = daily_user_database.get_streak(username)
    html_code = flask.render_template('leaderboard.html', top_players = top_players, points = points, daily_points = daily_points, rank = rank, daily_rank = daily_rank, streak = streak)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/versus', methods=['GET'])
def versus_func():
    users = user_database.get_players()
    username = flask.request.args.get('username')
    html_code = flask.render_template('versus.html', users=flask.json.dumps(users), username=username)
    response = flask.make_response(html_code)
    return response

@app.route('/create-challenge', methods=['POST'])
def create_challenge_route():
    challengee_id = flask.request.form['challengee_id'].strip()  # Trim whitespace
    users = user_database.get_players()  # Assuming this returns a list of usernames
    
    # Ensure challengee_id is not empty and exists in the users list
    if challengee_id == None or challengee_id not in users or challengee_id == auth.authenticate():
        response = {'status': 'error', 'message': 'Invalid challengee ID'}
        return flask.jsonify(response), 400  # Including a 400 Bad Request status code
    else:
        result = challenges_database.create_challenge(auth.authenticate(), challengee_id)
    
    # Handle the response from the database function
    if 'error' in result:
        return flask.jsonify({'status': 'error', 'message': result['error']}), 400 
    else:
        return flask.jsonify({'status': 'success', 'message': result['success'], 'challenge_id': result['challenge_id']}), 200

@app.route('/accept_challenge', methods=['POST'])
def accept_challenge_route():
    challenge_id = flask.request.form.get('challenge_id')
    result = challenges_database.accept_challenge(challenge_id)  # Assuming this returns some result
    if result == "accepted":
        flash('Challenge accepted successfully.')
    else:
        flash('Error accepting challenge.')
    return redirect(url_for('requests'))  # Assuming this is your route name

@app.route('/decline_challenge', methods=['POST'])
def decline_challenge_route():
    challenge_id = flask.request.form.get('challenge_id')
    result = challenges_database.decline_challenge(challenge_id)  # Assuming this returns some result
    if result == "declined":
        flash('Challenge declined successfully.')
    else:
        flash('Error declining challenge.')
    return redirect(url_for('requests'))

@app.route('/play_button', methods=['POST'])
def play_button():
    challenge_id = flask.request.form.get('challenge_id')
    user = auth.authenticate()
    status = challenges_database.get_playbutton_status(challenge_id, user)
    if status == None:
        challenges_database.update_playbutton_status(challenge_id, user)
        return redirect(url_for('start_challenge', challenge_id=challenge_id))
    elif status == True:
        challenges_database.update_finish_status(challenge_id, user)
        status = challenges_database.check_finish_status(challenge_id)
        if status['status'] == "finished":
            result = challenges_database.get_challenge_results(challenge_id)
            matches_database.complete_match(challenge_id, result['winner'], result['challenger_points'], result['challengee_points'])
            return redirect(url_for('requests'))
        else:
            return redirect(url_for('requests'))

@app.route('/start_challenge', methods=['GET'])
def start_challenge():
    challenge_id = flask.request.args.get('challenge_id')
    index = int(flask.request.args.get('index', 0))
    versusList = challenges_database.get_random_versus(challenge_id)

    if index < len(versusList):
        link = pictures_database.get_pic_info("link", versusList[index])
        html_code = flask.render_template('versusgame.html', challenge_id=challenge_id, index=index, link=link)
        response = flask.make_response(html_code)
        return response

@app.route('/end_challenge', methods=['POST'])
def end_challenge():
    challenge_id = flask.request.form.get('challenge_id')
    user = auth.authenticate()
    challenges_database.update_finish_status(challenge_id, user)
    status = challenges_database.check_finish_status(challenge_id)
    if status['status'] == "finished":
        result = challenges_database.get_challenge_results(challenge_id)
        matches_database.complete_match(challenge_id, result['winner'], result['challenger_points'], result['challengee_points'])
        return redirect(url_for('requests'))
    else:
        return redirect(url_for('requests'))
    
@app.route('/submit2', methods=['POST'])
def submit2():
    currLat = flask.request.form.get('currLat')  
    currLon = flask.request.form.get('currLon')
    points = 0
    if not currLat or not currLon:
        index = int(flask.request.form.get('index'))
        challenge_id = flask.request.form.get('challenge_id')
        distance = 0
        pic_status = versus_database.get_versus_pic_status(challenge_id, auth.authenticate(), index+1)
        if pic_status == False:
            versus_database.update_versus_pic_status(challenge_id, auth.authenticate(), index+1)
            versus_database.store_versus_pic_points(challenge_id, auth.authenticate(), index+1, points)
            versus_database.update_versus_points(challenge_id, auth.authenticate(), points)
        else:
            points = "Already submitted."
        index = int(index) + 1
        html_code = flask.render_template('versusresults.html', dis = distance, lat = None, lon = None, coor=None, index=index, challenge_id=challenge_id, points=str(points))
        response = flask.make_response(html_code)
        return response
    
    index = int(flask.request.form.get('index'))
    challenge_id = flask.request.form.get('challenge_id')
    time = int(flask.request.form.get('time'))
    versusList = challenges_database.get_random_versus(challenge_id)
    coor = pictures_database.get_pic_info("coordinates", versusList[index])
    distance = distance_func.calc_distance(currLat, currLon, coor)
    pic_status = versus_database.get_versus_pic_status(challenge_id, auth.authenticate(), index+1)
    if pic_status == False:
        points = versus_database.calculate_versus(distance, time)
        versus_database.store_versus_pic_points(challenge_id, auth.authenticate(), index+1, points)
        versus_database.update_versus_points(challenge_id, auth.authenticate(), points)
        versus_database.update_versus_pic_status(challenge_id, auth.authenticate(), index+1)
    else:
        points = "Already submitted."
    index = int(index) + 1
    html_code = flask.render_template('versusresults.html', dis = distance, lat = currLat, lon = currLon, coor=coor, index=index, challenge_id=challenge_id, points=str(points))
    response = flask.make_response(html_code)
    return response
    

@app.route('/versus_stats', methods=['GET'])
def versus_stats():
    challenge_id = flask.request.args.get('challenge_id')
    results = challenges_database.get_challenge_results(challenge_id)
    versusList = challenges_database.get_random_versus(challenge_id)
    pictures = [pictures_database.get_pic_info("link", pic) for pic in versusList]
    html_code = flask.render_template('versus_stats.html', results=results, images=pictures)
    response = flask.make_response(html_code)
    return response
