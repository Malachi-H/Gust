from random import randint
from typing import List, Tuple
from pygame.surface import Surface
import pygame

from PIL import Image
from pygame.event import Event
from screen_dimensions import ScreenDimensions
from button_type import ButtonType
from HelperFunctions import load_full_screen_image


class HomeScreen:
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
        self.MouseCollider = MouseCollider(mouse, self.display_surface)

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
        return buttons

    def check_for_and_handle_button_click(self, events, level_button):
        mouse_up = pygame.MOUSEBUTTONUP in [
            event.type for event in events
        ]  # Button Up to make detection rising edge
        if mouse_up:
            for button in ButtonType:
                if level_button.button_type == button:
                    self.button_pressed = button

    def detect_button_interaction(self, level_buttons, MouseCollider, events):
        for level_button in level_buttons:
            if pygame.sprite.collide_mask(MouseCollider, level_button):
                level_button.image = level_button.image_list["selected"]
                self.check_for_and_handle_button_click(events, level_button)
            else:
                level_button.image = level_button.image_list["unselected"]

    def update(self, events: List[Event]):
        self.display_surface.blit(self.main_screen, (0, 0))
        mouse = pygame.mouse.get_pos()
        self.level_buttons.update(events, self.MouseCollider)
        self.MouseCollider.update(mouse)
        self.detect_button_interaction(self.level_buttons, self.MouseCollider, events)


class Button(pygame.sprite.Sprite):
    """Sprite class to handle button interactions

    ### Parameters
    1. display_surface : Surface
            - The surface to render the button onto. ie. the screen
    2. button_type : ButtonType
            - identifies the button. Used for setting the appropriate image. eg. ButtonType.level_1
    """

    def __init__(
        self,
        button_type: ButtonType,
        display_surface: Surface,
        ScreenDimensions: ScreenDimensions,
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.display_surface = display_surface
        self.ScreenDimensions = ScreenDimensions
        self.image_list: dict[str, pygame.Surface] = self.import_images(button_type)
        self.image = self.image_list["unselected"]
        self.masks: dict[str, pygame.Mask] = self.create_masks(self.image_list)
        self.rect = self.image.get_rect()
        self.clicked = False
        self.button_type = button_type

    def create_masks(self, images):
        masks = {}
        for key, image in images.items():
            masks[key] = pygame.mask.from_surface(image)
        return masks

    def import_images(self, button_type: ButtonType) -> dict[str, Surface]:
        """Imports images into a dictionary. Images are full screen size with a transparent background. Mouse hover is detected using a mask which is generated from the images alpha values.

        ### Parameters
        1. button_type : ButtonType
                - The type of button to import images for. eg. ButtonType.level_1

        ### Returns:
            - Dict:
                - Keys:   'unselected', 'selected'
                - Values: Surface, Surface
        """

        if button_type == ButtonType.level_1:
            return {
                "unselected": load_full_screen_image(
                    self.ScreenDimensions,
                    "Assets\\Main Screen\\Level_Buttons\\level_1_button_high_res.png",
                    "Assets\\Main Screen\\Level_Buttons\\level_1_button.png",
                ),
                "selected": load_full_screen_image(
                    self.ScreenDimensions,
                    "Assets\\Main Screen\\Level_Buttons\\level_1_button_selected_high_res.png",
                    "Assets\\Main Screen\\Level_Buttons\\level_1_button_selected.png",
                ),
            }
        elif button_type == ButtonType.update:
            return {
                "unselected": load_full_screen_image(
                    self.ScreenDimensions,
                    "Assets\\Main Screen\\Settings_Buttons\\setting_update_high_res.png",
                    "Assets\\Main Screen\\Settings_Buttons\\setting_update.png",
                ),
                "selected": load_full_screen_image(
                    self.ScreenDimensions,
                    "Assets\\Main Screen\\Settings_Buttons\\setting_update_selected_high_res.png",
                    "Assets\\Main Screen\\Settings_Buttons\\setting_update_selected.png",
                ),
            }
        elif button_type == ButtonType.Resolution_1:
            return {
                "unselected": load_full_screen_image(
                    self.ScreenDimensions,
                    "Assets\\Main Screen\\Settings_Buttons\\resolution_1_high_res.png",
                    "Assets\\Main Screen\\Settings_Buttons\\resolution_1.png",
                ),
                "selected": load_full_screen_image(
                    self.ScreenDimensions,
                    "Assets\\Main Screen\\Settings_Buttons\\resolution_1_selected_high_res.png",
                    "Assets\\Main Screen\\Settings_Buttons\\resolution_1_selected.png",
                ),
            }
        elif button_type == ButtonType.Resolution_2:
            return {
                "unselected": load_full_screen_image(
                    self.ScreenDimensions,
                    "Assets\\Main Screen\\Settings_Buttons\\resolution_2_high_res.png",
                    "Assets\\Main Screen\\Settings_Buttons\\resolution_2.png",
                ),
                "selected": load_full_screen_image(
                    self.ScreenDimensions,
                    "Assets\\Main Screen\\Settings_Buttons\\resolution_2_selected_high_res.png",
                    "Assets\\Main Screen\\Settings_Buttons\\resolution_2_selected.png",
                ),
            }
        elif button_type == ButtonType.Resolution_3:
            return {
                "unselected": load_full_screen_image(
                    self.ScreenDimensions,
                    "Assets\\Main Screen\\Settings_Buttons\\resolution_3_high_res.png",
                    "Assets\\Main Screen\\Settings_Buttons\\resolution_3.png",
                ),
                "selected": load_full_screen_image(
                    self.ScreenDimensions,
                    "Assets\\Main Screen\\Settings_Buttons\\resolution_3_selected_high_res.png",
                    "Assets\\Main Screen\\Settings_Buttons\\resolution_3_selected.png",
                ),
            }

    def update(self, events, MouseCollider):
        self.display_surface.blit(self.image, self.rect)
        # self.check_mouse_interaction(events, MouseCollider)


class MouseCollider(pygame.sprite.Sprite):
    def __init__(self, mouse, display_surface):
        pygame.sprite.Sprite.__init__(self)
        self.display_surface = display_surface
        self.image = pygame.surface.Surface((10, 10))
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.center = mouse

    def update(self, mouse):
        self.rect.center = mouse
        # self.display_surface.blit(self.image, self.rect)
