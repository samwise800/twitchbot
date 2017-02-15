import channel
from channel import Channel
import db

db.setup()

c = Channel()
c.connect()
c.listen()
