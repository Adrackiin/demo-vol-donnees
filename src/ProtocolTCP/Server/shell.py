from .Protocol_TCP_server import Protocol_TCP_server
from .Terminal_server import Terminal

tcp = Protocol_TCP_server()
tcp.start_server("localhost", 25009)
Terminal(tcp)