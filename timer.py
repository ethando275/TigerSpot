import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
import database

def reset_game():

    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(database.reset_players, 'cron', hour=21, minute=58)

    #print("HELLO")

    #try:
        #while True:
            #time.sleep(2)
    #except (KeyboardInterrupt, SystemExit):
        #scheduler.shutdown()

def main():

    print(time.localtime())

if __name__ == '__main__':
    main()
