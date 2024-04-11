import sys
import admin
import argparse
import database
import datetime
import time
import threading


def timer():
    pic_changed = False
    while True: 
        now = datetime.datetime.now()
        if now.hour == 21 and now.minute == 32 and now.second == 0 and not pic_changed:
            database.reset_players()
            admin.pic_of_day()
            print('here')
            pic_changed = True
            time.sleep(60)


        elif now.minute != 32: 
            pic_changed = False
        
        time.sleep(1)

            

def main():
    parser = argparse.ArgumentParser(
        description="TigerSpot"
    )
    parser.add_argument(
        "port", type=int, help="the port at which the server should \
        listen"
    )

    try:
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print(e, file=sys.stderr)
        sys.exit(2)

    try:

        timer_thread = threading.Thread(target=timer)
        #stops thread when main program exits
        timer_thread.daemon = True
        timer_thread.start()
    
        admin.app.run(host='0.0.0.0', port=args.port, debug=False)
        

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
