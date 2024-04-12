import sys
import admin
import argparse

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
        admin.app.run(host='0.0.0.0', port=args.port, debug=True)
        
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
