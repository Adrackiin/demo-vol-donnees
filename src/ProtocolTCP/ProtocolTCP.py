from enum import Enum

# Flag | End | ........

PACKET_SIZE = 1024
HEADER_SIZE = 2
DATA_SIZE = PACKET_SIZE - HEADER_SIZE


class Flag(Enum):
    DATA = 0
    RAW_DATA = 1
