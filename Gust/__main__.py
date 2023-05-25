from time import sleep
import pygame
from window import Window
from player import Player


class Game:
    def __init__(self, window: Window) -> None:
        pygame.init()
        self.Window = window
        self.clock = pygame.time.Clock()

    def run(self):
        active = True
        while active:
            # pump = False augment is broken so event.get() can only be used once per frame with the lines result passed to other files
            events = pygame.event.get()
            for event in events:
                if (
                    event.type == pygame.QUIT
                    or pygame.key.get_pressed()[pygame.K_ESCAPE]
                ):
                    active = False

            self.Window.update(events, self.clock)
            pygame.display.update()
            self.clock.tick(60)


game = Game(Window())
game.run()
