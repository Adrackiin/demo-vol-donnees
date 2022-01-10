import os
import socket
from math import ceil

from ..ProtocolTCP import Flag, PACKET_SIZE, HEADER_SIZE, DATA_SIZE
from ..utils import file_is_present


class Protocol_TCP_client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connected = False
        self.data_size = PACKET_SIZE - HEADER_SIZE

    def connect(self, address, port):
        try:
            self.client.connect((address, port))
            self._connected = True
        except:
            raise ConnectionError(f"Cannot reach '{address}'.")

    def disconnect(self):
        self.client.close()
        self._connected = False

    def is_client_connected(self):
        return self._connected

    def send_file(self, file_name):
        size = os.path.getsize(file_name)
        self.send_msg(f"{file_name};{size}")
        file = open(file_name, "rb")
        if size > 1024:
            num = 0
            for i in range(ceil(size / 1024)):
                file.seek(num, 0)
                data = file.read(1024)
                self.client.send(data)
                num += 1024
        else:
            data = file.read()
            self.client.send(data)
        file.close()

    def receive_file(self):
        msg = self.receive_msg()
        msg_split = msg.strip().split(';')
        file_name = msg_split[0]
        size = int(msg_split[1])
        file = open(file_name, "wb")
        if size < 1024:
            msg_raw = self.receive_msg_raw()
            file.write(msg_raw)
        else:
            nb = ceil(size / 1024)
            for i in range(nb):
                msg_raw = self.receive_msg_raw()
                file.write(msg_raw)
        file.close()

    def get_file(self, file_name):
        if file_is_present(file_name):
            self.client.send("OK".encode())
            self.send_file(file_name)
        else:
            self.send_msg(f"File '{file_name}' doesn't exist")

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

