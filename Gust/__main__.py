from time import sleep
import pygame
from window import Window
from player import Player


class Game:
    def __init__(self):
        pass

    def run(self):
        pass


pygame.init()
Window = Window()
Window.screen
clock = pygame.time.Clock()
game = Game()
player = Player(Window.screen)

active = True
while active:
    # pump = False augment is broken so event.get() can only be used once per frame with the lines result passed to other files
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            active = False

    Window.screen.fill("white")
    player.update(events)
    pygame.display.update()
    clock.tick(60)
