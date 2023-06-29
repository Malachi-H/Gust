from typing import List
from pygame.surface import Surface
import pygame

from PIL import Image
from pygame.event import Event
from screen_dimensions import ScreenDimensions
from HelperFunctions import load_full_screen_image
from buttons import MouseCollider
from buttons import ButtonType, check_for_and_handle_button_click, Button


class HomeScreen:
    """Handles the visual elements of the home screen and the buttons on it. This includes creating the buttons and responding to button clicks.
    """
    def __init__(self, screen: Surface, ScreenDimensions: ScreenDimensions) -> None:
        self.display_surface = screen
        self.ScreenDimensions = ScreenDimensions
        self.main_screen = load_full_screen_image(
            self.ScreenDimensions,
            "Assets\\Main Screen\\Main_Screen_Background\\Main_screen_high_res.png",
            "Assets\\Main Screen\\Main_Screen_Background\\main_screen.png",
        )
        self.level_buttons: pygame.sprite.Group = self.create_buttons()
        self.button_pressed: (None | ButtonType) = None

        mouse = pygame.mouse.get_pos()
        self.MouseCollider = MouseCollider(
            mouse, self.display_surface, self.ScreenDimensions
        )

    def create_buttons(self):
        buttons = pygame.sprite.Group()
        # Level 1
        buttons.add(
            Button(
                button_type=ButtonType.level_1,
                display_surface=self.display_surface,
                ScreenDimensions=self.ScreenDimensions,
            )
        )
        # Update
        buttons.add(
            Button(
                button_type=ButtonType.update,
                display_surface=self.display_surface,
                ScreenDimensions=self.ScreenDimensions,
            )
        )
        # Resolution 1 (720x480)
        buttons.add(
            Button(
                button_type=ButtonType.Resolution_1,
                display_surface=self.display_surface,
                ScreenDimensions=self.ScreenDimensions,
            )
        )
        # Resolution 2 (360x240)
        buttons.add(
            Button(
                button_type=ButtonType.Resolution_2,
                display_surface=self.display_surface,
                ScreenDimensions=self.ScreenDimensions,
            )
        )
        # Resolution 3 (1440x960)
        buttons.add(
            Button(
                button_type=ButtonType.Resolution_3,
                display_surface=self.display_surface,
                ScreenDimensions=self.ScreenDimensions,
            )
        )
        buttons.add(
            Button(
                button_type=ButtonType.help_screen,
                display_surface=self.display_surface,
                ScreenDimensions=self.ScreenDimensions,
            )
        )
        return buttons

    def detect_button_interaction(self, level_buttons, MouseCollider, events):
        for level_button in level_buttons:
            if pygame.sprite.collide_mask(MouseCollider, level_button):
                level_button.image = level_button.image_dict["selected"]
                button_clicks = check_for_and_handle_button_click(events, level_button)
                if button_clicks != None:
                    self.button_pressed = button_clicks
            else:
                level_button.image = level_button.image_dict["unselected"]

    def update(self, events: List[Event]):
        self.display_surface.blit(self.main_screen, (0, 0))
        mouse = pygame.mouse.get_pos()
        self.level_buttons.update()
        self.MouseCollider.update(mouse)
        self.detect_button_interaction(self.level_buttons, self.MouseCollider, events)
