import os
import socket
import time
from enum import Enum
from math import ceil

# Flag | End | ........

PACKET_SIZE = 32
HEADER_SIZE = 2
DATA_SIZE = PACKET_SIZE - HEADER_SIZE


class Flag(Enum):
    DATA = 0
    RAW_DATA = 1
    ERROR = 2
    ACK = 3
    COMMAND = 4


class Connection:
    def __init__(self, connection=socket.socket(socket.AF_INET, socket.SOCK_STREAM), connected=False):
        self.connection = connection
        self._connected = connected

    def connect_to_server(self, address, port):
        """
        Connexion à un serveur
        """
        try:
            self.connection.connect((address, port))
            self._connected = True
        except:
            raise ConnectionError(f"Cannot reach '{address}'.")

    def disconnect(self):
        """
        Déconnection de la connexion
        """
        self.connection.close()
        self._connected = False

    def is_connected(self):
        """
        Renvoie vrai s'il y a une connexion
        """
        return self._connected

    def send_packet(self, flag, it):
        """
        Envoie un message sous la forme de plusieurs paquets
        Prend en argument un générateur pour générer les différents paquets
        """
        def send(packet_chunk, end):
            """
            Envoie un paquet sous la forme
                FLAG END data
            """
           
            packet = b''.join(
                [flag.value.to_bytes(1, 'little'),
                 b'\1' if end else b'\0',
                 packet_chunk.encode() if flag != Flag.RAW_DATA else packet_chunk])
            # Debug
            print("send=", packet, "\n")
            if len(packet) > PACKET_SIZE:
                raise ValueError(f"Size of packet ({len(packet)}) > {PACKET_SIZE}")
            self.connection.send(packet)

        # Il faut savoir quel est le dernier morceau à envoyer pour préciser le flag END
        iterator = iter(it)
        try:
            current = next(iterator)
        except StopIteration as e:
            current = ""
        for chunk in iterator:
            send(current, False)
            current = chunk
        send(current, True)

    def receive_packet(self):
        """
        Reçoit un message envoyé sous plusieurs paquets
        """
        end = False
        error = ""
        while not end:
            packet = self.connection.recv(PACKET_SIZE)
            # Debug
            print("receive=", packet, "\n")
            flag = Flag(packet[0])
            end = packet[1] == 1
            msg = packet[HEADER_SIZE:]
            if flag == Flag.ERROR:
                error += msg.decode()
            else:
                yield msg.decode() if flag != Flag.RAW_DATA else msg
        if error != "":
            raise ValueError(error)

    def send_msg(self, msg, flag=Flag.DATA):
        """
        Envoie un message
        """
        def split_msg():
            """
            Découpe un message en plusieurs morceaux
            """
            if flag == Flag.RAW_DATA:
                for i in range(0, len(msg), DATA_SIZE):
                    yield msg[i:i + DATA_SIZE]
            else:
                data_encoded_length = 0
                to_send = ""
                for c in msg:
                    encoded = c.encode()
                    if data_encoded_length + len(encoded) > DATA_SIZE:
                        yield to_send[0:data_encoded_length]
                        to_send = to_send[data_encoded_length:-1]
                        data_encoded_length = 0
                    to_send += c
                    data_encoded_length += len(encoded)
                if to_send:
                    yield to_send

        self.send_packet(flag, split_msg())

    def send_ack(self):
        """
        Envoie une confirmatiton
        """
        self.send_msg("Le code c'est la loire", Flag.ACK)

    def send_error(self, error):
        """
        Envoie une erreur
        """
        self.send_msg("Erreur client\n" + "{0}".format(error), Flag.ERROR)

    def send_command(self, action, *args):
        """
        Envoie une commande sous la forme 'action arg1 args2...'
        Les espaces ne séparant pas d'arguments sont précédés d'un '\'
        """
        command = f"{action} "
        for arg in args:
            if arg:
                if type(arg) == list:
                    arg = arg[0]
                command += arg.replace("\\", "\\\\").replace(" ", "\\ ")
                command += ' '
        self.send_msg(command, Flag.COMMAND)

    def receive_msg(self):
        """
        Reçoit un message
        """
        return "".join(list(self.receive_packet()))

    def send_file(self, path_file):
        """
        Envoie un fichier
        """
        def send_file_chunk(file):
            """
            Découpe le fichier en plusieurs morceaux
            """
            pos = 0
            nb_iteration = ceil(size / DATA_SIZE)
            for i in range(nb_iteration):
                file.seek(pos, 0)
                data = file.read(DATA_SIZE)
                yield data
                pos += DATA_SIZE

        size = os.path.getsize(path_file)
        file_name = path_file.split('/')[-1]
        # Envoie des informations sur le fichier, nom + taille
        self.send_msg(f"{file_name};{size}")
        file_to_send = open(path_file, "rb")
        self.send_packet(Flag.RAW_DATA, send_file_chunk(file_to_send))
        file_to_send.close()

    def receive_file(self, file_destination):
        """
        Reçoit un fichier
        """
        file_to_receive = self.receive_msg()
        file_info = file_to_receive.strip().split(';')
        file_name = file_info[0]
        size = int(file_info[1])
        file = open(f"{file_destination}/{file_name}", "wb")
        for chunk in self.receive_packet():
            file.write(chunk)
        file.close()
        return file_name
