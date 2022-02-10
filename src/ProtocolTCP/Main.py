import sys

from .Client.target import start_client
from .Server.shell import start_server

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("1 argument missing: client / server")
        exit(0)
    if sys.argv[1] == "client":
        start_client(sys.argv[2:])
    elif sys.argv[1] == "server":
        start_server(sys.argv[2:])
