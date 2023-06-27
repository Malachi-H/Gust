from time import sleep
from typing import Type
import pygame
from screen_dimensions import ScreenDimensions
from window import Window
from player import Player


class Game:
    def __init__(self, Window: Type[Window]) -> None:
        pygame.init()
        self.ScreenDimensions = ScreenDimensions()
        self.window = self.make_window()
        self.clock = pygame.time.Clock()

    def make_window(self):
        return Window(self.ScreenDimensions)

    def run(self):
        active = True
        while active:
            # pump = False augment is broken so event.get() can only be used once per frame with the lines result passed to other files
            events = pygame.event.get()
            for event in events:
                if (
                    event.type == pygame.QUIT
                    or pygame.key.get_pressed()[pygame.K_LCTRL]
                    and pygame.key.get_pressed()[pygame.K_q]
                    or pygame.key.get_pressed()[pygame.K_RCTRL]
                    and pygame.key.get_pressed()[pygame.K_q]
                ):
                    active = False

            self.window.update(events, self.clock)
            if self.window.restart_screen == True:
                pygame.display.quit()
                pygame.display.init()
                self.window = self.make_window()
            pygame.display.update()
            self.clock.tick(60)


game = Game(Window)
game.run()
