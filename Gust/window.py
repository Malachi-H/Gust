from time import sleep
import pygame
import os
from typing import Tuple
import level
from pygame.event import Event 
import HelperFunctions



common_display_resolutions: list[Tuple[int, int]] = [
    (720, 480),
    (1280, 720),
    (1920, 1080),
    (3840, 2160),
]
screen_dimension = common_display_resolutions[0]
# screen_dimension = (4,3)

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
        self.screen = pygame.display.set_mode(screen_dimension, self.screen_flags)
        self.Level = level.Level(self.screen)
        

        
    
    def update(self, events: list[Event]) -> None:
        self.Level.update(events)
        