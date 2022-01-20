import socket

from ..Connection import Connection
from ..utils import file_is_present, path_is_correct


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

    def get_file(self, file_to_get, destination_path):
        if not path_is_correct(destination_path):
            raise FileNotFoundError(f"{destination_path} not found")
        try:
            self.client.send_msg(f"GET {file_to_get}")
            self.client.receive_msg()
            self.client.receive_file(destination_path)
        except Exception:
            raise

    def put_file(self, file_to_send, destination_path):
        if not file_is_present(file_to_send):
            raise FileNotFoundError(f"File '{file_to_send}' doesn't exist")
        try:
            self.client.send_msg(f"PUT {destination_path}")
            self.client.receive_msg()
            self.client.send_file(file_to_send)
        except Exception:
            raise
