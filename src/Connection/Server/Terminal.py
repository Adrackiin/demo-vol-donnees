import os
import time
import traceback

from .Server import Server
from ..utils import file_is_present, get_path, parse_command


class Terminal(Server):
    def __init__(self, address, port):
        super().__init__()
        self.start_server(address, port)
        self.connect_client()

        self.client.send_msg("PWD")
        msg = self.client.receive_msg()

        # Chemin absolu
        self.current_path = msg.strip()
        # Dossier actuel
        self.current_directory = self.current_path.split('/')[-1]

        while self.is_server_connected():
            # Gestion utilisateur
            try:
                command = input(f"{self.current_directory}$ ")
            except (EOFError, KeyboardInterrupt):
                print()
                command = "close"
            if len(command) > 0:
                args = parse_command(command)
                action = args[0].lower()
                try:
                    # Appel de la fonction correspondante à l'action
                    eval(f"self.{action}")(args)
                except (AttributeError, SyntaxError):
                    print("Unknown command")
                except ParseError as error:
                    print(f"Error in command {action}: {error}")
                except Exception:
                    print("\n", traceback.format_exc())

    def put(self, args):
        """
        Envoie un fichier
        Commande: 'PUT <fichier> <destination> [file_to_replace]'
        """
        file_to_send = get_path(".", args[1])
        destination_path = get_path(self.current_path, args[2] if len(args) > 2 else "")
        replace = ""
        if len(args) > 3:
            replace = args[3]
        self.put_file(file_to_send, destination_path, replace)

    def get(self, args):
        """
        Reçoit un fichier
        Commande: 'GET <fichier> [<destination>]'
        """
        file_to_get = get_path(self.current_path, args[1])
        destination_path = get_path(".", args[2] if len(args) > 2 else "")
        self.get_file(file_to_get, destination_path)

    def end(self, args):
        self.client.send_command("END")
        time.sleep(1)
        self.disconnect_client()
        self.connect_client()

    def close(self, args):
        if self.is_client_connected():
            self.client.send_command("END")
            self.disconnect_client()
        self.close_server()

    def ls(self, args):
        self.client.send_command("LS")
        print(self.client.receive_msg())

    def cd(self, args):
        self.client.send_command("CD", args[1:])
        msg = self.client.receive_msg()
        self.current_path = msg.strip()
        self.current_directory = self.current_path.split('/')[-1]

    def pwd(self, args):
        self.client.send_command("PWD")
        print(self.client.receive_msg())


class ParseError(Exception):
    pass
