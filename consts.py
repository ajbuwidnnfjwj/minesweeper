import pygame

# color RGB info
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 69, 0)
GOLD = (255, 125, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GROUND_BROWN1 = (229, 194, 159)
GROUND_BROWN2 = (215, 184, 153)
GRASS_GREEN1 = (162, 209, 73)
GRASS_GREEN2 = (170, 215, 81)

# window size
WIDTH = 600
HEIGHT = 600 + 100

# game info
BOMBNUM = 50

FIELD_WIDTH = 20
FIELD_HEIGHT = 20

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
window.fill(WHITE)
pygame.display.set_caption("minesweep")
font = pygame.font.Font(None, 50)
UI_font = pygame.font.Font(None, 30)
