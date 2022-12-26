from random import *
import consts

bombcord = []  # bomb coordinates
field = [[0 for _ in range(20)] for _ in range(20)]
opened = [[False for _ in range(20)] for _ in range(20)]
flagged = [[False for _ in range(20)] for _ in range(20)]


def GenerateGame(pos):
    x = pos[0]//30
    y = (pos[1]-100)//30
    while len(bombcord) < consts.BOMBNUM:
        rand_cord = [randrange(20) for _ in range(2)]
        if x-1 <= rand_cord[0] <= x+1 and y-1 <= rand_cord[1] <= y+1:
            continue
        else:
            if rand_cord not in bombcord:
                bombcord.append(rand_cord)
    print(sorted(bombcord))
    print(len(bombcord))
    for i in bombcord:
        field[i[1]][i[0]] = 'b'


def CountNearBomb__init__():
    for y in range(20):
        for x in range(20):
            if field[y][x] == 'b':
                continue
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    elif 0 <= (dx+x) < 20 and 0 <= (dy+y) < 20:
                        if field[y+dy][x+dx] == 'b':
                            field[y][x] += 1
    for i in field:
        print(*i)


def CountNearFlag(x, y):
    near_flag_count = 0

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            elif 0 <= (dx+x) < 20 and 0 <= (dy+y) < 20:
                if flagged[y+dy][x+dx]:
                    near_flag_count += 1
    return near_flag_count
