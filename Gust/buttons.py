from enum import Enum, auto
import pygame
from pygame.surface import Surface
from HelperFunctions import load_full_screen_image
from screen_dimensions import ScreenDimensions


class ButtonType(Enum):
    level_1 = auto()
    update = auto()
    Resolution_1 = auto()
    Resolution_2 = auto()
    Resolution_3 = auto()
    help_screen = auto()
    help_home = auto()
    help_next = auto()


class MouseCollider(pygame.sprite.Sprite):
    def __init__(self, mouse, display_surface, ScreenDimensions: ScreenDimensions):
        pygame.sprite.Sprite.__init__(self)
        self.display_surface = display_surface
        self.ScreenDimensions = ScreenDimensions
        size = int(10 * ScreenDimensions.scale_factor)
        self.image = pygame.surface.Surface((size, size))
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.center = mouse

    def update(self, mouse):
        self.rect.center = mouse
        # self.display_surface.blit(self.image, self.rect)


def check_for_and_handle_button_click(events, level_button) -> ButtonType:
    mouse_up = pygame.MOUSEBUTTONUP in [
        event.type for event in events
    ]  # Button Up to make detection rising edge
    if mouse_up:
        for button in ButtonType:
            if level_button.button_type == button:
                return button


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
        self.button_type = button_type
        self.image_dict: dict[str, pygame.Surface] = self.import_images(
            self.button_type
        )
        self.image = self.image_dict["unselected"]
        self.masks: dict[str, pygame.Mask] = self.create_masks(self.image_dict)
        self.rect = self.image.get_rect()
        self.clicked = False

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
        elif button_type == ButtonType.help_screen:
            return {
                "unselected": load_full_screen_image(
                    self.ScreenDimensions,
                    "Assets\\Main Screen\\Help Buttons\\help_screen_high_res.png",
                    "Assets\\Main Screen\\Help Buttons\\help_screen.png",
                ),
                "selected": load_full_screen_image(
                    self.ScreenDimensions,
                    "Assets\\Main Screen\\Help Buttons\\help_screen_high_res_selected.png",
                    "Assets\\Main Screen\\Help Buttons\\help_screen_selected.png",
                ),
            }
        elif button_type == ButtonType.help_home:
            return {
                "unselected": load_full_screen_image(
                    self.ScreenDimensions,
                    "Assets\\Help Screen\\help_screen_home_high_res.png",
                    "Assets\\Help Screen\\help_screen_home.png",
                ),
                "selected": load_full_screen_image(
                    self.ScreenDimensions,
                    "Assets/Help Screen/help_screen_home_selected_high_res.png",
                    "Assets/Help Screen/help_screen_home_selected.png",
                ),
            }
        elif button_type == ButtonType.help_next:
            return {
                "unselected": load_full_screen_image(
                    self.ScreenDimensions,
                    "Assets\\Help Screen\\help_screen_next_high_res.png",
                    "Assets\\Help Screen\\help_screen_next.png",
                ),
                "selected": load_full_screen_image(
                    self.ScreenDimensions,
                    "Assets/Help Screen/help_screen_next_selected_high_res.png",
                    "Assets/Help Screen/help_screen_next_selected.png",
                ),
            }

    def update(self, MouseCollider):
        self.display_surface.blit(self.image, self.rect)
