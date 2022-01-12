import time
import traceback

from .Server import Server
from ..utils import file_is_present, concatenate_path


class Terminal(Server):
    def __init__(self, address, port):
        super().__init__()
        self.start_server(address, port)
        self.connect_client()

        self.client.send_msg("PWD")
        msg = self.client.receive_msg()

        # Full path
        self.current_path = msg.strip()
        # Only directory
        self.current_directory = self.current_path.split('/')[-1]

        while self.is_server_connected():
            try:
                command = input(f"{self.current_directory}$ ")
            except (EOFError, KeyboardInterrupt):
                print()
                command = "close"
            args = command.strip().split(' ')
            args[0] = args[0].lower()
            action = args[0]
            try:
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
        Commande: 'PUT <fichier> <destination>'
        """
        self.put_file(args[1], concatenate_path(self.current_path, args[2]))

    def get(self, args):
        """
        Reçoit un fichier
        Commande: 'GET <fichier> [<destination>]'
        """
        print(args)
        self.get_file(f"{self.current_path}/{args[1]}", args[2] if len(args) > 2 else "")

    def end(self, args):
        self.client.send_msg("END")
        time.sleep(1)
        self.disconnect_client()
        self.connect_client()

    def close(self, args):
        if self.is_client_connected():
            self.client.send_msg("END")
            self.disconnect_client()
        self.close_server()

    def ls(self, args):
        self.client.send_msg("LS")
        print(self.client.receive_msg())

    def cd(self, args):
        if len(args) <= 1 or args[1] == "":
            raise ParseError("No directory specified")
        self.client.send_msg(" ".join(args))
        msg = self.client.receive_msg()
        self.current_path = msg.strip()
        self.current_directory = self.current_path.split('/')[-1]

    def pwd(self, args):
        self.client.send_msg("PWD")
        print(self.client.receive_msg())


class ParseError(Exception):
    pass
