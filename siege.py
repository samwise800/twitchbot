import time

adds = {}
ongoing = False
stage = 0
timer = 0
recruited = 0
recruit_timer = 0


def start():
    global ongoing, recruited, recruit_timer, timer, stage
    ongoing = True
    recruited = 0
    recruit_timer = 0
    timer = time.time()
    stage = 1
    print("Siege has started")


def reset():
    global ongoing, stage, timer, adds, recruited, recruit_timer
    ongoing = False
    stage = 0
    timer = 0
    adds = {}
    recruited = 0
    recruit_timer = 0
