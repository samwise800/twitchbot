import time
import re
import commands
from user import User
import select


class Listener:

    def __init__(self, channel):
        self.channel = channel

    def listen(self):
        p = re.compile(r"^:(?P<USER>\w+)!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
        while True:
            self.channel.s.setblocking(0)
            ready = select.select([self.channel.s], [], [], 0.2)
            if ready[0]:
                response_raw = self.channel.s.recv(4096).decode("utf-8")
                responses = response_raw.replace("\r","").split("\n")
                for response in responses:
                    response = response.rstrip()
                    if (response != ""):
                        if (response == "PING :tmi.twitch.tv"):
                            print(response)
                            self.channel.s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                            print("PONG sent")
                        elif ("PRIVMSG" in response):
                            user_name = p.search(response).group('USER')
                            user = User(user_name)
                            message = p.sub("", response).rstrip()
                            t = time.strftime("%H:%M:%S")
                            #print("[" + t + "] " + user.name + ": " + message)
                            if message.startswith("!"):
                                print("[" + t + "] " + user.name + ": " + message)
                            commands.do(message, user)
                        else:
                            print(response)
            commands.cycle()
            self.channel.do_queue()
            time.sleep(0.1)
