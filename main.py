import pygame
import numpy as np
from ch8 import Ch8State

SCALE = 6

ch8 = Ch8State()
ch8.load_ram("roms/programs/Fishie [Hap, 2005].ch8")

pygame.init()
screen = pygame.display.set_mode((64*SCALE, 32*SCALE))
CLOCK, t = pygame.USEREVENT + 1, 2
pygame.time.set_timer(CLOCK, t)

while True:
    if pygame.event.get(pygame.QUIT): break
    for e in pygame.event.get():
        if e.type == CLOCK:
            ch8.step()

    arr = np.full((32 , 64), 255, dtype="int")
    mask = ch8.display.get_display()
    arr[~mask] = 0

    surface = pygame.transform.scale(pygame.surfarray.make_surface(arr.T), (64*SCALE, 32*SCALE))
    screen.blit(surface, (0, 0))
    pygame.display.flip()
