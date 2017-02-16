import socket
import cfg
from listener import Listener
import time
from collections import deque


last_chat = 0
queue = deque()

class Channel:

    def __init__(self):
        self.s = None
        self.l = Listener(self)
        global c
        c = self

    def connect(self):
        self.s = socket.socket()
        self.s.connect((cfg.HOST, cfg.PORT))
        self.s.send("PASS {}\r\n".format(cfg.PASS).encode())
        self.s.send("NICK {}\r\n".format(cfg.NAME).encode())
        self.s.send("JOIN #{}\r\n".format(cfg.CHAN).encode())

        connected = False
        while not connected:
            response = self.s.recv(1024).decode("utf-8")
            print(response)
            if "End of /NAMES list" in response:
                connected = True
        print("Connected to #" + cfg.CHAN)

    def chat(self, msg):
        global last_chat
        if self.can_chat():
            self.s.send("PRIVMSG #{} :{}\r\n".format(cfg.CHAN, msg).encode())
            last_chat = time.time()
        elif cfg.QUEUE:
            print("message added to queue")
            queue.append(msg)
        else:
            print("message discarded")

    def listen(self):
        self.l.listen()

    def do_queue(self):
        if cfg.QUEUE and len(queue)>0:
            if self.can_chat():
                msg = queue.popleft()
                self.chat(msg)
                print("message sent from queue")

    def can_chat(self):
        return (time.time() - last_chat) > cfg.DELAY

