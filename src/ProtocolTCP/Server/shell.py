import sys

from .Terminal import Terminal


def start_server(args):
    Terminal("localhost", 25000 if len(args) <= 0 else int(args[0]))


if __name__ == "__main__":
    start_server(sys.argv[1:])
