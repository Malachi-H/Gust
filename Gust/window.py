from enum import Enum, auto
import pygame
import os
from typing import Tuple
from level import Level
from pygame.event import Event
from screen_dimensions import ScreenDimensions
from home_screen import HomeScreen
from splash_screen import SplashScreen
import re as RegEx
from help_screen import HelpScreen
from buttons import ButtonType


class Window:
    """The window class handles what GUI to display at what time. It also handles the effects of button interactions, such as changing the GUI or the resolution.
    """
    def __init__(
        self, ScreenDimensions: ScreenDimensions, is_first_start_up: bool
    ) -> None:
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.screen_flags = pygame.RESIZABLE | pygame.SCALED
        self.ScreenDimensions = ScreenDimensions
        self.screen = pygame.display.set_mode(
            tuple(self.ScreenDimensions.screen_dimensions), self.screen_flags
        )
        pygame.display.set_caption("Gust")
        self.HomeScreen = HomeScreen(
            screen=self.screen, ScreenDimensions=self.ScreenDimensions
        )
        self.is_first_start_up = is_first_start_up
        self.Level = Level(screen=self.screen, ScreenDimensions=self.ScreenDimensions)
        self.SplashScreen = SplashScreen(self.screen, self.ScreenDimensions)
        self.HelpScreen = HelpScreen(self.screen, self.ScreenDimensions)
        self.GUI = GUI_Type.splash_screen
        self.restart_screen = False
        self.level_complete = False
        self.ticks_at_level_complete = (
            -1
        )  # -1 used as sentinel value for when level is not complete

    @property
    def current_resolution(self) -> Tuple[int, int]:
        return self.screen.get_size()

    def update(self, events: list[Event], clock) -> None:
        if self.GUI == GUI_Type.splash_screen:
            if self.SplashScreen.stop_displaying == True:
                self.GUI = GUI_Type.home_screen
                self.is_first_start_up = False
            if self.is_first_start_up == True:
                self.SplashScreen.update()
            else:
                self.GUI = GUI_Type.home_screen

        if self.GUI == GUI_Type.home_screen:
            self.HomeScreen.update(events)

            self.handle_buttons()
        if self.GUI == GUI_Type.help_screen:
            self.HelpScreen.update(events)
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.GUI = GUI_Type.home_screen
                self.HelpScreen.current_help_screen = self.HelpScreen.help_screen_1
            self.handle_buttons()
        if self.GUI == GUI_Type.level_screen:
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
            self.ticks_at_level_complete != -1
            and self.level_complete == True
            and pygame.time.get_ticks() * dt - self.ticks_at_level_complete * dt
            > 2250 * dt
        ):
            # return to home screen and reset level
            self.ticks_at_level_complete = -1
            self.level_complete = False
            self.Level.level_complete = False
            self.Level.restart_level()
            self.GUI = GUI_Type.home_screen

    def handle_buttons(self):
        if self.HomeScreen.button_pressed == ButtonType.level_1:
            self.HomeScreen.button_pressed = None  # reset button_pressed so that it doesn't trigger again when screen is reloaded
            self.GUI = GUI_Type.level_screen
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
        if self.HomeScreen.button_pressed == ButtonType.update:
            self.HomeScreen.button_pressed = None  # reset button_pressed so that it doesn't trigger again when screen is reloaded
            with open("custom_settings.txt", "r+") as f:
                resolution = RegEx.match(
                    r"Resolution = \(\d+, \d+\)", f.read()
                )  # get resolution from file
                if resolution == None:  # if resolution is not in file, add it
                    f.seek(0)
                    f.write("Resolution = (720, 480)")
                f.seek(0)
                altered_file = RegEx.sub(
                    r"Resolution = \(\d+, \d+\)",
                    f"Resolution = {self.current_resolution}",
                    f.read(),
                )  # replace resolution in file with current resolution
                f.seek(0)
                f.truncate()
                f.write(altered_file)
        if self.HomeScreen.button_pressed == ButtonType.help_screen:
            self.HelpScreen.current_help_screen = self.HelpScreen.help_screen_1
            self.HomeScreen.button_pressed = None  # reset button_pressed so that it doesn't trigger again when screen is reloaded
            self.GUI = GUI_Type.help_screen
        if self.HelpScreen.button_pressed == ButtonType.help_home:
            self.HelpScreen.button_pressed = None  # reset button_pressed so that it doesn't trigger again when screen is reloaded
            self.GUI = GUI_Type.home_screen
            self.HelpScreen.current_help_screen = self.HelpScreen.help_screen_1
        if self.HelpScreen.button_pressed == ButtonType.help_next:
            self.HelpScreen.button_pressed = None  # reset button_pressed so that it doesn't trigger again when screen is reloaded
            self.HelpScreen.current_help_screen = self.HelpScreen.help_screen_2


class GUI_Type(Enum):
    # available GUIs to switch between
    splash_screen = auto()
    home_screen = auto()
    level_screen = auto()
    help_screen = auto()
