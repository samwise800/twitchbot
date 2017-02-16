import channel
from channel import Channel
import db
import time

db.setup()

c = Channel()
c.connect()
c.listen()

#spam = input("Whaty to spam> ")
#while True:
#    c.chat(spam)
#    time.sleep(5)
#    c.chat(spam + " .")
#    time.sleep(5)