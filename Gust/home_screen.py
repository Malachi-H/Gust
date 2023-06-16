from random import randint
from typing import List
from pygame.surface import Surface
import pygame
from screen_dimensions import screen_dimensions, scale_factor
from PIL import Image
from pygame.event import Event
from button_type import ButtonType
from HelperFunctions import load_full_screen_image


class HomeScreen:
    def __init__(self, screen: Surface) -> None:
        self.display_surface = screen
        self.main_screen = load_full_screen_image(
            "Assets\\Main Screen\\Main_screen_high_res.png",
            "Assets\\Main Screen\\Main_Screen_Background\\main_screen.png",
        )
        self.level_buttons: pygame.sprite.Group = self.create_level_buttons()
        self.button_pressed: (None | ButtonType) = None

        mouse = pygame.mouse.get_pos()
        self.MouseCollider = MouseCollider(mouse, self.display_surface)

    def create_level_buttons(self):
        buttons = pygame.sprite.Group()
        buttons.add(
            Button(
                button_type=ButtonType.level_1,
                display_surface=self.display_surface,
            )
        )
        buttons.add(
            Button(
                button_type=ButtonType.settings,
                display_surface=self.display_surface,
            )
        )
        return buttons

    def check_for_and_handle_button_click(self, events, level_button):
        mouse_up = pygame.MOUSEBUTTONUP in [
            event.type for event in events
        ]  # Button Up to make detection rising edge
        if mouse_up:
            if level_button.button_type == ButtonType.level_1:
                self.button_pressed = ButtonType.level_1
            elif level_button.button_type == ButtonType.settings:
                self.button_pressed = ButtonType.settings

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
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.display_surface = display_surface
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
                    "Assets\\Main Screen\\Level_Buttons\\level_1_button_high_res.png",
                    "Assets\\Main Screen\\Level_Buttons\\level_1_button.png",
                ),
                "selected": load_full_screen_image(
                    "Assets\\Main Screen\\Level_Buttons\\level_1_button_selected_high_res.png",
                    "Assets\\Main Screen\\Level_Buttons\\level_1_button_selected.png",
                ),
            }
        elif button_type == ButtonType.settings:
            return {
                "unselected": load_full_screen_image(
                    "Assets\\Main Screen\\setting_update_high_res.png",
                    "Assets\\Main Screen\\Settings_Buttons\\setting_update.png",
                ),
                "selected": load_full_screen_image(
                    "Assets\\Main Screen\\Settings_Buttons\\setting_update_selected_high_res.png",
                    "Assets\\Main Screen\\Settings_Buttons\\setting_update_selected.png",
                ),
            }

    def create_solid_colour_image(self, size):
        # ! Deprecated
        image = pygame.surface.Surface(
            ([dimension * scale_factor for dimension in size])
        )
        image.fill(color=(randint(0, 255), randint(0, 255), randint(0, 255)))
        return image

    def create_solid_colour_rect(self, pos):
        # ! Deprecated
        rect = self.image.get_rect()  # type: ignore
        rect.topleft = int(pos[0] * scale_factor), int(pos[1] * scale_factor)
        return rect

    # def check_mouse_interaction(self, events: List[Event], mouse):
    #     mouse_down = pygame.MOUSEBUTTONDOWN in [event.type for event in events]
    #     if pygame.sprite.collide_mask(MouseCollider, self.masks["unselected"]):
    #     if self.rect.collidepoint(mouse):
    #         self.display_image = self.images["selected"]
    #         if mouse_down:
    #             self.clicked = True
    #         else:
    #             self.clicked = False
    #     else:
    #         self.display_image = self.images["unselected"]

    # def mask_collidepoint(self, mouse):
    #     collision_surface = pygame.surface.Surface((10,10))
    #     collision_surface.fill('red')
    #     collision_rect = collision_surface.get_rect()
    #     collision_rect.center = mouse
    #     pygame.sprite.collide_mask(self, collision_rect)

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
