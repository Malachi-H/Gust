import os
from time import sleep
import pygame, sys
from window import Window


class Game:
    def __init__(self):
        pass

    def run(self):
        pass


pygame.init()
Window = Window()
clock = pygame.time.Clock()
game = Game()


active = True
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        elif event.type == pygame.VIDEORESIZE:
            Window.constrain_aspect_ratio_and_min_size()
    Window.screen.fill("black")
    pygame.display.update()
    clock.tick(60)
