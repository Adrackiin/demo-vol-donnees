import socket

from ..Connection import Connection
from ..utils import file_is_present


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_connected = False
        self.client: Connection = None

    def start_server(self, address, port):
        self.server.bind((address, port))
        self._server_connected = True
        self.server.listen(1)

    def connect_client(self):
        print("Waiting connection")
        self.client = Connection(self.server.accept()[0], True)

    def disconnect_client(self):
        self.client.disconnect()

    def close_server(self):
        self.server.close()
        self._server_connected = False

    def is_client_connected(self):
        return self.client.is_connected()

    def is_server_connected(self):
        return self._server_connected

    def get_file(self, file_to_get, to_put_in):
        self.client.send_msg(f"GET {file_to_get}")
        self.client.receive_file(to_put_in)

    def put_file(self, file_to_send, destination_path):
        if file_is_present(file_to_send):
            self.client.send_msg(f"PUT {destination_path}")
            self.client.send_file(file_to_send)
        else:
            raise Exception(f"File '{file_to_send}' doesn't exist")
