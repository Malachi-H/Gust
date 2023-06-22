from enum import Enum, auto
from time import sleep
import pygame
import os
from typing import Tuple
from level import Level
from pygame.event import Event
import HelperFunctions
from screen_dimensions import ScreenDimensions
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

    def __init__(self, ScreenDimensions) -> None:
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.screen_flags = pygame.RESIZABLE | pygame.SCALED
        self.ScreenDimensions = ScreenDimensions
        self.screen = pygame.display.set_mode(
            self.ScreenDimensions.screen_dimensions, self.screen_flags
        )
        self.HomeScreen = HomeScreen(
            screen=self.screen, ScreenDimensions=self.ScreenDimensions
        )
        self.Level = Level(screen=self.screen, ScreenDimensions=self.ScreenDimensions)
        self.GUI = GUI_Type.home_screen
        self.restart_screen = False

    def update(self, events: list[Event], clock) -> None:
        if self.GUI == GUI_Type.home_screen:
            self.HomeScreen.update(events)

            self.new_method()

        if self.GUI == GUI_Type.level:
            self.Level.update(events, clock)
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.GUI = GUI_Type.home_screen

    def new_method(self):
        if self.HomeScreen.button_pressed == ButtonType.level_1:
            self.HomeScreen.button_pressed = None  # reset button_pressed so that it doesn't trigger again when screen is reloaded
            self.GUI = GUI_Type.level
        if self.HomeScreen.button_pressed == ButtonType.Resolution_1:
            self.HomeScreen.button_pressed = None  # reset button_pressed so that it doesn't trigger again when screen is reloaded
            print("Resolution 1")
            self.ScreenDimensions.screen_dimensions = (720, 480)
            self.restart_screen = True
        if self.HomeScreen.button_pressed == ButtonType.Resolution_2:
            self.HomeScreen.button_pressed = None  # reset button_pressed so that it doesn't trigger again when screen is reloaded
            print("Resolution 2")
            self.ScreenDimensions.screen_dimensions = (360, 240)
            self.restart_screen = True
        if self.HomeScreen.button_pressed == ButtonType.Resolution_3:
            self.HomeScreen.button_pressed = None  # reset button_pressed so that it doesn't trigger again when screen is reloaded
            print("Resolution 3")
            self.ScreenDimensions.screen_dimensions = (1440, 960)
            self.restart_screen = True


class GUI_Type(Enum):
    home_screen = auto()
    level = auto()
