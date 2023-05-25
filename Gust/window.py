from time import sleep
import pygame
import os
from typing import Tuple
import level
from pygame.event import Event
import HelperFunctions
from screen_dimensions import screen_dimensions
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
        self.GUI = HomeScreen(screen=self.screen)

    def update(self, events: list[Event], clock) -> None:
        self.GUI.update(events)
