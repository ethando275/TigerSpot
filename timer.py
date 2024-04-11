import datetime
import apscheduler
import database

def reset_game():

   schedule.every().day.at("23:59:59").do(database.reset_players())





