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
    def __init__(self, ScreenDimensions: ScreenDimensions) -> None:
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.screen_flags = pygame.RESIZABLE | pygame.SCALED
        self.ScreenDimensions = ScreenDimensions
        self.screen = pygame.display.set_mode(
            tuple(self.ScreenDimensions.screen_dimensions), self.screen_flags
        )
        self.HomeScreen = HomeScreen(
            screen=self.screen, ScreenDimensions=self.ScreenDimensions
        )
        self.Level = Level(screen=self.screen, ScreenDimensions=self.ScreenDimensions)
        self.GUI = GUI_Type.home_screen
        self.restart_screen = False
        self.level_complete = False
        self.ticks_at_level_complete = (
            -1
        )  # -1 used as sentinel value for when level is not complete

    def update(self, events: list[Event], clock) -> None:
        if self.GUI == GUI_Type.home_screen:
            self.HomeScreen.update(events)

            self.handle_home_screen_buttons()

        if self.GUI == GUI_Type.level:
            self.Level.update(events, clock)
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.GUI = GUI_Type.home_screen
            if self.Level.level_complete:
                self.handle_level_complete(clock)

    def handle_level_complete(self, clock):
        dt = clock.get_time() / 1000
        if self.level_complete == False:
            self.level_complete = True
            self.ticks_at_level_complete = pygame.time.get_ticks()
        if (
            self.ticks_at_level_complete != -1 and self.level_complete == True
            and pygame.time.get_ticks() * dt - self.ticks_at_level_complete * dt
            > 2250 * dt
        ):
            # return to home screen and reset level
            self.ticks_at_level_complete = -1
            self.level_complete = False
            self.Level.level_complete = False
            self.Level.restart_level()
            self.GUI = GUI_Type.home_screen

    def handle_home_screen_buttons(self):
        if self.HomeScreen.button_pressed == ButtonType.level_1:
            self.HomeScreen.button_pressed = None  # reset button_pressed so that it doesn't trigger again when screen is reloaded
            self.GUI = GUI_Type.level
        if self.HomeScreen.button_pressed == ButtonType.Resolution_1:
            self.HomeScreen.button_pressed = None  # reset button_pressed so that it doesn't trigger again when screen is reloaded
            self.ScreenDimensions.screen_dimensions = (720, 480)
            self.restart_screen = True
        if self.HomeScreen.button_pressed == ButtonType.Resolution_2:
            self.HomeScreen.button_pressed = None  # reset button_pressed so that it doesn't trigger again when screen is reloaded
            self.ScreenDimensions.screen_dimensions = (360, 240)
            self.restart_screen = True
        if self.HomeScreen.button_pressed == ButtonType.Resolution_3:
            self.HomeScreen.button_pressed = None  # reset button_pressed so that it doesn't trigger again when screen is reloaded
            self.ScreenDimensions.screen_dimensions = (1440, 960)
            self.restart_screen = True


class GUI_Type(Enum):
    home_screen = auto()
    level = auto()
