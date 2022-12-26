import pygame
import sys
from consts import window
import consts
import cells
import functions as fn
import time

sys.setrecursionlimit(2**31-1)

# drawing field
for x in range(20):
    for y in range(20):
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

if __name__ == "__main__":
    first_click = True
    start_time = time.time()

    while first_click:

        pygame.display.update()
        fn.UpdateInfo(start_time, first_click)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if 100 <= pos[1] <= 700:
                    print(pos[0]//20, (pos[1]-100)//20)
                    cells.GenerateGame(list(pos))
                    cells.CountNearBomb__init__()
                    fn.MouseControl(event, pos)
                    start_time = time.time()
                    first_click = False

            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    while True:
        pygame.display.update()
        fn.UpdateInfo(start_time, first_click)
        if fn.keep and not fn.fail:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    fn.MouseControl(event, pos)

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        else:
            break

    print("end")
    pygame.display.update()
    fn.UpdateInfo(start_time, first_click)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
