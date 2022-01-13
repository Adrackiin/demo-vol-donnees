import os

from ..Connection import DATA_SIZE, Flag, Connection
from ..utils import concatenate_path


class Client:
    def __init__(self, address, port):
        self.working_directory = os.getcwd().replace('\\', '/')
        self.connection = Connection()
        try:
            self.connection.connect_to_server(address, port)
        except:
            exit(0)
        while self.connection.is_connected():
            msg = self.connection.receive_msg()
            args = msg.strip().split(' ')
            action = args[0].lower()
            try:
                eval(f"self.{action}")(args)
            except (AttributeError, SyntaxError):
                self.connection.send_msg("Unknown command")
            except ParseError as error:
                self.connection.send_msg(f"Error in command {action}: {error}")

    def put(self, args):
        """
        Reçoit un fichier du serveur
        Commande reçu: 'PUT <destination>'
        """
        self.connection.receive_file(args[1])

    def get(self, args):
        """
        Envoie un fichier au server
        Commande reçu: 'GET <fichier>'
        """
        self.connection.send_file(args[1])

    def end(self, args):
        """
        Se déconnecte du serveur
        """
        self.connection.disconnect()

    def ls(self, args):
        """
        Envoie la liste des fichiers du répertoire courant
        Commande reçu: 'LS [<dossier>]'
        """

        def send(directory_to_show):
            to_send = ""
            for file in os.listdir(directory_to_show):
                type_file = "d" if os.path.isdir(f"{directory_to_show}/{file}") else "f"
                data = f"{type_file} {file}\n"
                to_send += data
                if len(data) >= DATA_SIZE:
                    yield to_send[0:DATA_SIZE]
                    to_send = data[DATA_SIZE:-1]
            if to_send != "":
                yield to_send

        self.connection.send_packet(Flag.DATA, send(concatenate_path(self.working_directory, args[1] if len(args) > 1 else "")))

    def cd(self, args):
        """
        Change de dossier courant
        Commande reçu: 'CD <dossier>'
        """
        if len(args) == 0:
            raise ParseError("No directory specified")
        current = '' if args[1][0] == '/' else self.working_directory
        for directory in args[1].split('/'):
            if not os.path.isdir(f"{current}/{directory}"):
                raise ParseError("Incorrect path")
            if directory == '..':
                current = '/'.join(current.split('/')[0:-1])
                if current.count('/') == 0:
                    current += '/'
            elif directory != '.':
                current += ('/' if not current.endswith('/') else '') + directory
        self.working_directory = current
        self.connection.send_msg(self.working_directory)

    def pwd(self, args):
        """
        Affiche le dossier courant
        Commande reçu: 'PWD'
        """
        self.connection.send_msg(self.working_directory)


class ParseError(Exception):
    pass
