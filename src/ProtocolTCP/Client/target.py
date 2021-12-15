from .Protocol_TCP_client import Protocol_TCP_client
from .Terminal_client import Terminal

tcp = Protocol_TCP_client()
tcp.connect("localhost", 25009)
Terminal(tcp)
