import pygame, sys


class Game:
    def __init__(self):
        pass

    def run(self):
        pass


pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

active = True
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
    screen.fill("black")
    pygame.display.update()
    clock.tick(60)
