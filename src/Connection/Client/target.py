import sys

from .Client import Client
from ..Connection import Connection


def start_client(args):
    Client("localhost", 25000 if len(args) <= 0 else int(args[0]))


if __name__ == "__main__":
    start_client(sys.argv[1:])
