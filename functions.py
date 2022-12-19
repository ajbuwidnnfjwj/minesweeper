import pygame
import consts
from consts import window, font, UI_font
import cells
import os
import time

left_bomb = consts.BOMBNUM
flag_num = 0

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "img")

fail = False
keep = True


# every function arguments should handled in functions
# ex) do not change tuple "pos" outside of functions


def CallColors(x) -> tuple:
    if x == 1:
        return consts.BLUE
    elif x == 2:
        return consts.GREEN
    elif x == 3:
        return consts.RED
    elif x == 4:
        return consts.PURPLE
    else:
        return consts.BLACK


def BombCounting(x, y) -> None:
    global flag_num, left_bomb

    flag_num += 1
    if cells.field[y][x] == 'b':
        left_bomb -= 1


def Printer(x, y):
    if cells.field[y][x] == 'b':
        mine_img = pygame.image.load(
            os.path.join(image_path, "mine.png"))
        window.blit(mine_img, (x*30 + 5, y*30 + 100 + 5))
    elif cells.field[y][x]:
        text = font.render("{}".format(
            cells.field[y][x]), True, CallColors(cells.field[y][x]))
        window.blit(text, (x*30 + 5, y*30 + 100))


def Opener(x, y) -> None:
    if x % 2 and y % 2:
        pygame.draw.rect(window, consts.GROUND_BROWN1, [
            30*x, 30*y + 100, 30, 30])
    elif not x % 2 and y % 2:
        pygame.draw.rect(window, consts.GROUND_BROWN2, [
            30*x, 30*y + 100, 30, 30])
    elif x % 2 and (not y % 2):
        pygame.draw.rect(window, consts.GROUND_BROWN2, [
            30*x, 30*y + 100, 30, 30])
    else:
        pygame.draw.rect(window, consts.GROUND_BROWN1, [
            30*x, 30*y + 100, 30, 30])


def Closer(x, y):
    if x % 2 and y % 2:
        pygame.draw.rect(window, consts.GRASS_GREEN1, [
                         30*x, 30*y + 100, 30, 30])
    elif not x % 2 and y % 2:
        pygame.draw.rect(window, consts.GRASS_GREEN2, [
            30*x, 30*y + 100, 30, 30])
    elif x % 2 and (not y % 2):
        pygame.draw.rect(window, consts.GRASS_GREEN2, [
            30*x, 30*y + 100, 30, 30])
    else:
        pygame.draw.rect(window, consts.GRASS_GREEN1, [
            30*x, 30*y + 100, 30, 30])


def NumberClicked(double_time, x, y):
    pass_time = 0

    while pass_time < 0.3:
        pass_time = time.time() - double_time
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if pos[0]//30 == x and (pos[1]-100)//30 == y:
                    if cells.field[y][x] == cells.CountNearFlag(x, y) and cells.opened[y][x]:
                        for dy in range(-1, 2):
                            for dx in range(-1, 2):
                                if 0 <= (x+dx) < 20 and 0 <= (y+dy) < 20:
                                    Dig(x+dx, y+dy)


def ShowAns():
    for y in range(20):
        for x in range(20):
            if cells.field[y][x] == 'b':
                mine_img = pygame.image.load(
                    os.path.join(image_path, "mine.png"))
                mine_img = pygame.transform.scale(mine_img, (30, 30))
                window.blit(mine_img, (x*30, y*30 + 100))
            elif cells.flagged[y][x]:
                pygame.draw.rect(window, consts.BLACK, [
                    30*x, 30*y + 100, 30, 30])
                text = font.render("{}".format(
                    cells.field[y][x]), True, CallColors(cells.field[y][x]))
                window.blit(text, (x*30 + 5, y*30 + 100))


def Dig(x, y):
    global keep, fail

    # check if bomb-cell is clicked
    if cells.field[y][x] == 'b' and not cells.flagged[y][x]:
        ShowAns()
        fail = True
        keep = False

    if not cells.opened[y][x]:
        cells.opened[y][x] = True
        Opener(x, y)
        Printer(x, y)

        if cells.field[y][x] == 0:
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if not dx and not dy:
                        continue
                    elif 0 <= (x+dx) < 20 and 0 <= (y+dy) < 20:
                        if not cells.opened[y+dy][x+dx] and cells.field[y+dy][x+dx] != 'b':
                            Dig(x+dx, y+dy)


def SetFlag(x, y) -> bool:
    global flag_num, keep, fail, left_bomb

    if not cells.opened[y][x]:
        cells.opened[y][x] = True
        cells.flagged[y][x] = True
        flag_img = pygame.image.load(
            os.path.join(image_path, "flag.png"))
        window.blit(flag_img, (x*30 + 5, y*30 + 100 + 4))
        BombCounting(x, y)
    else:
        if cells.flagged[y][x]:
            Closer(x, y)
            flag_num -= 1
            cells.opened[y][x] = False
            cells.flagged[y][x] = False
            if cells.field[y][x] == 'b':
                left_bomb += 1
    keep = not End()


def MouseControl(event, pos):
    # pos -> tuple for clicked position
    if pos[1] < 100:
        return 0

    if event.button == 1 and not cells.opened[(pos[1]-100)//30][pos[0]//30]:
        Dig(pos[0]//30, (pos[1]-100)//30)
    elif event.button == 1 and cells.opened[(pos[1]-100)//30][pos[0]//30]:
        double_time = time.time()
        NumberClicked(double_time, pos[0]//30, (pos[1]-100)//30)
    elif event.button == 3:
        SetFlag(pos[0]//30, (pos[1]-100)//30)
    print(left_bomb)


def End():
    global left_bomb, flag_num
    print()
    if left_bomb == 0 and flag_num == consts.BOMBNUM:
        return True
    else:
        return False


def UpdateInfo(start_time, first_click) -> None:
    global keep, fail
    spent_time = 0

    if first_click:
        pass
    else:
        spent_time = time.time()

    sec = UI_font.render("time: {}s".format(int(spent_time-start_time) if int(spent_time-start_time) >= 0 else 0),
                         True, consts.BLACK, consts.WHITE)
    window.blit(sec, (450, 20))

    if keep and not fail:
        text = UI_font.render("Left Bomb: {0:02d}".format(
            consts.BOMBNUM-flag_num if (consts.BOMBNUM-flag_num) >= 0 else 0), True, consts.BLACK, consts.WHITE)
        window.blit(text, (10, 20))
    elif not keep and not fail:
        pygame.draw.rect(window, consts.WHITE, [
            0, 0, 300, 100])
        text = UI_font.render(
            "Success", True, consts.BLACK, consts.WHITE)
        window.blit(text, (10, 20))
    elif not keep and fail:
        pygame.draw.rect(window, consts.WHITE, [
            0, 0, 300, 100])
        text = UI_font.render(
            "Fail", True, consts.RED, consts.WHITE)
        window.blit(text, (20, 20))
