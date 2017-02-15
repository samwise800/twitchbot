import sqlite3

db = sqlite3.connect('data.db')


def purge():
    db.execute("DELETE FROM usrdata")
    db.commit()
    db.execute("vacuum")
    print("usrdata table purged")

def setup():
    db.execute("CREATE TABLE IF NOT EXISTS usrdata (user varchar(255), money int)")
