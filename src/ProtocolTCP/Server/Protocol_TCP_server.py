import os
import socket
from math import ceil

from ..ProtocolTCP import Flag, PACKET_SIZE, HEADER_SIZE, DATA_SIZE
from ..utils import file_is_present


class Protocol_TCP_server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_connected = False
        self._server_connected = False
        self.data_size = PACKET_SIZE - HEADER_SIZE

    def start_server(self, address, port):
        self.server.bind((address, port))
        self.server.listen(1)
        self._server_connected = True
        self.connect_client()

    def connect_client(self):
        print("Waiting connection")
        client, address = self.server.accept()
        self.client = client
        self._client_connected = True

    def disconnect_client(self):
        self.client.close()
        self._client_connected = False

    def close_server(self):
        self.server.close()
        self._server_connected = False

    def is_client_connected(self):
        return self._client_connected

    def is_server_connected(self):
        return self._server_connected

    def send_file(self, file_name, dest_path):
        size = os.path.getsize(file_name)
        self.send_msg(f"{dest_path}/{file_name};{size}")
        file = open(file_name, "rb")
        if size > 1024:
            num = 0
            pourcent = 0
            nb = ceil(size / 1024)
            for i in range(nb):
                tmp = i / nb * 100 // 10
                if pourcent != tmp:
                    pourcent = tmp
                    print(f"{pourcent * 10}%")
                file.seek(num, 0)
                data = file.read(1024)
                self.client.send(data)
                num += 1024
        else:
            data = file.read()
            self.client.send(data)
        file.close()

    def receive_file(self, file_name):
        msg = self.receive_msg()
        msg_split = msg.strip().split(';')
        size = int(msg_split[1])
        file = open(file_name, "wb")
        if size < 1024:
            msg_raw = self.receive_msg_raw()
            file.write(msg_raw)
        else:
            nb = ceil(size / 1024)
            pourcent = 0
            for i in range(nb):
                tmp = i / nb * 100 // 10
                if pourcent != tmp:
                    pourcent = tmp
                    print(f"{pourcent * 10}%")
                msg_raw = self.receive_msg_raw()
                file.write(msg_raw)
        file.close()

    def get_file(self, command, current_path):
        command_split = command.strip().split(' ')
        action = command_split[0]
        file_name = " ".join(command_split[1:])
        command = f"{action} {current_path}/{file_name}"
        self.send_msg(command)
        msg = self.receive_msg()
        if msg == "OK":
            self.receive_file(file_name)
        else:
            print(msg)

    def put_file(self, file_name, command, dest_path):
        if file_is_present(file_name):
            self.send_msg(command)
            self.send_file(file_name, dest_path)
        else:
            raise Exception(f"File '{file_name}' doesn't exist")

    def send_msg_packet(self, flag, it):
        def send(packet_chunk, end):
            self.client.send(b''.join(
                [flag.value.to_bytes(1, 'little'),
                 b'\1' if end else b'\0',
                 packet_chunk.encode() if flag == Flag.DATA else packet_chunk]))

        iterator = iter(it)
        current = next(iterator)
        for chunk in iterator:
            send(current, False)
            current = chunk
        send(current, True)

    def send_msg(self, msg):
        def split_msg():
            for i in range(0, len(msg), PACKET_SIZE - HEADER_SIZE):
                yield msg[i:i + DATA_SIZE]

        self.send_msg_packet(Flag.DATA, split_msg())

    def send_err(self, err):
        self.client.send("{0}".format(err).encode())

    def receive_msg_packet(self):
        end = False
        while not end:
            packet = self.client.recv(PACKET_SIZE)
            flag = Flag(packet[0])
            end = packet[1] == 1
            msg = packet[HEADER_SIZE:]
            yield msg.decode() if flag == Flag.DATA else msg
    
    def receive_msg(self):
        return "".join(list(self.receive_msg_packet()))

    def receive_msg_raw(self):
        msg = self.client.recv(1024)
        return msg
