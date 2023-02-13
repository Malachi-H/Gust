from time import sleep
import pygame
import os
from pygame.surface import Surface
from typing import Tuple

resolutions: list[Tuple[int, int]] = [
    (720, 480),
    (1280, 720),
    (1920, 1080),
    (3840, 2160),
]
screen_dimension = resolutions[0]


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
        self.screen = pygame.display.set_mode(
            screen_dimension, self.screen_flags
        )
