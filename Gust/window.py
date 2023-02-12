from time import sleep
import pygame
import os
from pygame.surface import Surface
from typing import  Tuple

resolutions: list[Tuple[int, int]] = [
    (720, 480),
    (1280, 720),
    (1920, 1080),
    (3840, 2160),
]
display_screen_dimension = resolutions[2]


class Window:
    """The Screen class is used to create the window and handle resizing.
    ...

    Functions:
    - constrain_aspect_ratio_and_min_size():
    - center_window()

    Attributes:
    - original_values
    """

    def __init__(self) -> None:
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.display_screen_flags = pygame.RESIZABLE | pygame.SCALED
        self.display_screen = pygame.display.set_mode(
            display_screen_dimension, self.display_screen_flags
        )

    def constrain_aspect_ratio_and_min_size(self) -> None:
        width, height = self.display_screen.get_size()
        height = width / 16 * 9
        pygame.display.set_mode((width, height), self.display_screen_flags)

    def center_window(self) -> None:
        #! This is not working
        """Center the window on the display. Centring required reinitializing the display."""
        size = self.display_screen.get_size()
        pygame.display.quit()
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.display_screen = pygame.display.set_mode(size, self.display_screen_flags)
        
