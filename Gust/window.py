import pygame
import os

resolutions = [
    (720, 480),
    (1280, 720),
    (1920, 1080),
    (3840, 2160),
]
screen_dimensions = resolutions[1]


class Window:
    """The Screen class is used to create the window and handle resizing.
    Functions:
        - constrain_aspect_ratio_and_min_size

    """

    def __init__(self):
        self.screen = pygame.display.set_mode(screen_dimensions, pygame.RESIZABLE)
        self.center_window()

    def constrain_aspect_ratio_and_min_size(self):
        width, height = self.screen.get_size()
        height = width / 16 * 9
        pygame.display.set_mode((width, height), pygame.RESIZABLE)

    def center_window(self):
        """Center the window on the display. Centring required reinitializing the display."""
        screen_dimensions = self.screen.get_size()
        pygame.display.quit()
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.screen = pygame.display.set_mode(screen_dimensions, pygame.RESIZABLE)
