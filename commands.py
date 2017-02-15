import re
from random import random
from user import User
import cfg
import channel
import time
from db import db
import siege


def chat(msg):
    channel.c.chat(msg)


def do(msg, user):

    if "TriHard" in msg:
        user.set_money_rel(1)
        print("{} now has {} money".format(user.name, user.get_money()))

    if msg == "!{}".format(cfg.UNIT):
        user.chat("you have {} {}".format(user.get_money(), cfg.UNIT))

    if msg.startswith("!gamble"):
        p = re.compile(r"^!gamble (?P<n>\d+)")
        if p.search(msg):
            bet = int(p.search(msg).group('n'))
            if user.get_money() >= bet:
                if random() < 0.5:
                    user.set_money_rel(bet)
                    user.chat("you won the bet and now have {} {}".format(user.get_money(), cfg.UNIT))
                    #print("{} won {} in a bet".format(user.name, str(bet)))
                else:
                    user.set_money_rel(-bet)
                    user.chat("you lost the bet and now have {} {}".format(user.get_money(), cfg.UNIT))
                    #print("{} lost {} in a bet".format(user.name, str(bet)))
            else:
                user.chat("you don't have enough money")

    if msg.startswith("!spawn") and user.is_owner():
        p = re.compile(r"^!spawn @?(?P<u>\w+) (?P<n>\d+)")
        if p.search(msg):
            user_name = p.search(msg).group('u')
            to_user = User(user_name)
            n = int(p.search(msg).group('n'))
            to_user.set_money_rel(n)
            user.chat("spawned @{} {} {}".format(to_user.name, n, cfg.UNIT))

    if msg.startswith("!give"):
        p = re.compile(r"^!give @?(?P<u>\w+) (?P<n>\d+)")
        if p.search(msg):
            print("ye")
            user_name = p.search(msg).group('u')
            print(user_name)
            to_user = User(user_name)
            n = int(p.search(msg).group('n'))
            to_user.set_money_rel(n)
            user.set_money_rel(-n)
            user.chat("gave @{} {} {}".format(to_user.name, n, cfg.UNIT))
            print("{} gave {} {}".format(user.name, to_user.name, str(n)))

    if msg.startswith("!top") or msg.startswith("!leaderboard") or msg.startswith("!scores"):
        c = db.execute("SELECT * FROM usrdata ORDER BY money DESC LIMIT 5")
        str = "Biggest slave owners: |"
        n = 1
        for user_name,money in c.fetchall():
            str += " ({}) {}: {} {} |".format( n, user_name, money, cfg.UNIT)
            n += 1
        chat(str)

    if msg.startswith("!add"):
        p = re.compile(r"^!add (?P<n>\d+)")
        if p.search(msg):
            if siege.ongoing:
                bet = int(p.search(msg).group('n'))
                if user.get_money() >= bet:
                    siege.adds[user.name] = bet
                    chat("{} added {} {}!".format(user.name, bet, cfg.UNIT))
                    print("{} added {}".format(user.name, bet))
                else:
                    user.chat("You don't have that many {}!".format(cfg.UNIT))
                    print("{} tried to add but didn't have enough".format(user.name))
            else:
                user.chat("There is no siege going on. Type !siege to vote to start one")


    if msg == "!siege":
        siege.recruited += 1;

        if siege.recruited == 1:
            chat("{} has voted to start a siege of a TriHard village! Type !siege to join. "
                 "{} seconds left to recruit {} more people ".format(user.name, cfg.RECRUIT_TIME, cfg.PEOPLE_PER_RAID-1))
            siege.recruit_timer = time.time();
            print("raid {}/{}".format(siege.recruited, cfg.PEOPLE_PER_RAID))

        elif 1 < siege.recruited < cfg.PEOPLE_PER_RAID:
            chat("{} has joined the voted to start a siege of a TriHard village! Type !siege to join.")
            print("raid {}/{}".format(siege.recruited, cfg.PEOPLE_PER_RAID))

        elif siege.recruited == cfg.PEOPLE_PER_RAID:
            print("raid {}/{}".format(siege.recruited, cfg.PEOPLE_PER_RAID))
            chat("The vote to raid a TriHard village has passed! Type !add and the number of "
                 "slaves you want to send.")
            siege.start()

    if msg == "!siegef" and user.is_owner():
        siege.start()


def cycle():

    if siege.recruit_timer > 0 and time.time() - siege.recruit_timer >= cfg.RECRUIT_TIME:
        siege.reset()
        chat("Failed to recruit enough people in time for the siege.")
        print("Siege aborted, failed to recruit enough people")

    if siege.ongoing:

        if time.time() - siege.timer > cfg.RAID_TIME/2 and siege.stage < 2:
            chat("The siege on the TriHard villiage will begin in {} seconds. "
                 "Type !add and the number of slaves you want to send".format(cfg.RAID_TIME/2))
            siege.stage = 2
            print("siege stage 2")

        if time.time() - siege.timer > cfg.RAID_TIME - 5 and siege.stage < 3:
            chat("5 seconds until the siege happens! WutFace")
            siege.stage = 3
            print("siege stage 3")

        if time.time() - siege.timer > cfg.RAID_TIME:

            total = sum(siege.adds.values())
            won = random() < 0.5

            if won:
                chat("PogChamp The siege on the TriHard village was successful! {} villagers "
                     "were taken as slaves".format(total * cfg.RAID_REWARD_MULT))
                print("================")
                print("siege won")
                print("{} slaves won".format(total * cfg.RAID_REWARD_MULT))
                print("siege is over")
                print("================")

            else:
                chat("NotLikeThis The siege on the TriHard village failed with no survivors! {} slaves were lost".format(total))
                print("================")
                print("siege lost")
                print("{} slaves lost".format(total))
                print("siege is over")
                print("================")

            for user_name, bet in siege.adds.items():
                user = User(user_name)
                if won:
                    user.set_money_rel(bet * cfg.RAID_REWARD_MULT)
                    print("{} bet {} slaves, giving {}".format(user.name, bet, bet*cfg.RAID_REWARD_MULT))
                else:
                    user.set_money_rel(-bet)
                    print("{} bet {} slaves, removing {}".format(user.name, bet, bet))
            print("================")
            siege.reset()




