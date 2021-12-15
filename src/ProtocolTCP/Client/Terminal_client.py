import os

from .Protocol_TCP_client import Protocol_TCP_client
from ..ProtocolTCP import DATA_SIZE, Flag


class Terminal:
    def __init__(self, tcp: Protocol_TCP_client):
        self.working_directory = os.getcwd().replace('\\', '/')
        self.tcp = tcp
        while tcp.is_client_connected():
            msg = tcp.receive_msg()
            msg_split = msg.strip().split(' ')
            action = msg_split[0].lower()
            args = msg_split[1:]
            try:
                eval(f"self.{action}")(args)
            except (AttributeError, SyntaxError):
                self.tcp.send_msg("Unknown command")
            except ParseError as error:
                self.tcp.send_msg(f"Error in command {action}: {error}")

    def put(self, args):
        self.tcp.receive_file()

    def get(self, args):
        self.tcp.get_file(" ".join(args))

    def end(self, args):
        self.tcp.disconnect()

    def ls(self, args):
        def send():
            to_send = ""
            for file in os.listdir(self.working_directory):
                type_file = "d" if os.path.isdir(f"{self.working_directory}/{file}") else "f"
                data = f"{type_file} {file}\n"
                if len(data) < DATA_SIZE:
                    to_send += data
                else:
                    yield to_send[0:DATA_SIZE]
                    to_send = data[DATA_SIZE:-1]
            if to_send != "":
                yield to_send

        self.tcp.send_msg_packet(Flag.DATA, send())

    def cd(self, args):
        if len(args) == 0:
            raise ParseError("No directory specified")
        current = '' if args[0][0] == '/' else self.working_directory
        for directory in args[0].split('/'):
            if not os.path.isdir(f"{current}/{directory}"):
                raise ParseError("Incorrect path")
            if directory == '..':
                current = '/'.join(current.split('/')[0:-1])
                if current.count('/') == 0:
                    current += '/'
            elif directory != '.':
                current += ('/' if not current.endswith('/') else '') + directory
        self.working_directory = current
        self.tcp.send_msg("OK")

    def pwd(self, args):
        self.tcp.send_msg(self.working_directory)


class ParseError(Exception):
    pass
