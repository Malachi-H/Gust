from enum import Enum, auto
from time import sleep
import pygame
import os
from typing import Tuple
import level
from pygame.event import Event
import HelperFunctions
from screen_dimensions import screen_dimensions
from button_type import ButtonType
from home_screen import HomeScreen


class Window:
    """The Screen class is used to create the window and handle resizing.
    ...

    Functions:
    - None

    Attributes:
    - screen
    - screen_flags
    """

    def __init__(self) -> None:
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.screen_flags = pygame.RESIZABLE | pygame.SCALED
        self.screen = pygame.display.set_mode(screen_dimensions, self.screen_flags)
        self.HomeScreen = HomeScreen(screen=self.screen)
        self.level = level.Level(screen=self.screen)
        self.GUI = GUI_Type.home_screen

    # def switch_GUI_to_level(self):
    #     self.HomeScreen = level.Level(screen=self.screen)

    def update(self, events: list[Event], clock) -> None:
        if self.GUI == GUI_Type.home_screen:
            self.HomeScreen.update(events)

            if self.HomeScreen.button_pressed == ButtonType.level_1:
                self.GUI = GUI_Type.level

        if self.GUI == GUI_Type.level:
            self.level.update(events, clock)


class GUI_Type(Enum):
    home_screen = auto()
    level = auto()
