from db import db
import cfg
import channel
#from main import get_channel

class User:

    def __init__(self, name):
        self.money = 0
        if name.startswith("@"):
            self.name = name[1:]
        else:
            self.name = name
        self.setup_data()

    def setup_data(self):
        c = db.execute("SELECT * FROM usrdata WHERE user=?", [self.name])
        if c.fetchone() is None:
            print("Creating data for user: {}".format(self.name))
            db.execute("INSERT INTO usrdata (user,money) VALUES (?,?)", [self.name, cfg.STARTING_MONEY])
            db.commit()

    def get_money(self):
        c = db.execute("SELECT money FROM usrdata WHERE user=?", [self.name])
        return int(c.fetchone()[0])

    def set_money(self, money):
        db.execute("UPDATE usrdata SET money=? WHERE user=?", [money, self.name])
        db.commit()

    def set_money_rel(self, rel_amount):
        self.set_money(self.get_money() + rel_amount)

    def is_owner(self):
        return self.name in cfg.OWNERS

    def chat(self, msg):
        channel.c.chat("@{} {}".format(self.name, msg))

