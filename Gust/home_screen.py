from random import randint
from typing import List
from pygame.surface import Surface
import pygame
from screen_dimensions import screen_dimensions, scale_factor
from PIL import Image
from pygame.event import Event
from button_type import ButtonType


class HomeScreen:
    def __init__(self, screen: Surface) -> None:
        self.display_surface = screen
        self.main_screen = self.load_full_screen_image(
            "Assets\\Main Screen\\main_screen.png"
        )
        self.level_buttons: pygame.sprite.Group = self.create_level_buttons()
        self.button_pressed: None | ButtonType = None

    def load_full_screen_image(self, path):
        py_main_screen = pygame.image.load(path)
        size = py_main_screen.get_size()
        if size[0] != screen_dimensions[0] or size[1] != screen_dimensions[1]:
            # Resized to display size dimensions
            with Image.open(path) as pil_main_screen:
                pil_main_screen_resized = pil_main_screen.resize((screen_dimensions))
                pil_main_screen_resized.save("Assets\\Main Screen\\main_screen.png")

            # Overwrite with resized image
            py_main_screen = pygame.image.load(path)
        return py_main_screen

    def create_level_buttons(self):
        buttons = pygame.sprite.Group()
        buttons.add(
            Button(
                button_type=ButtonType.level_1,
                display_surface=self.display_surface,
                pos=(40, 280),
                size=(128, 40),
            )
        )
        buttons.add(
            Button(
                button_type=ButtonType.settings,
                display_surface=self.display_surface,
                pos=(550, 400),
                size=(128, 40),
            )
        )
        return buttons

    def handle_button_clicks(self, level_buttons):
        for button in level_buttons:
            if button.clicked:
                if button.button_type == ButtonType.level_1:
                    self.button_pressed = ButtonType.level_1
                elif button.button_type == ButtonType.settings:
                    self.button_pressed = ButtonType.settings

    def update(self, events: List[Event]):
        self.display_surface.blit(self.main_screen, (0, 0))
        mouse = pygame.mouse.get_pos()
        self.level_buttons.update(events, mouse)
        self.handle_button_clicks(self.level_buttons)


class Button(pygame.sprite.Sprite):
    """
    ## __init__:

        display_surface: Surface

        pos: tuple[int,int]
            Number of pixels from the top left corner of the display surface (assume screen size of 720,480)

        size: tuple[int,int]
            Number of pixels wide and tall the button is
            (assume screen size of 720,480)
    """

    def __init__(
        self,
        button_type: ButtonType,
        display_surface: Surface,
        pos: tuple[int, int],
        size: tuple[int, int],
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.display_surface = display_surface
        self.image = self.create_solid_colour_image(size)
        self.rect = self.create_rect(pos)
        self.clicked = False
        self.button_type = button_type

    def create_solid_colour_image(self, size):
        image = pygame.surface.Surface(
            ([dimension * scale_factor for dimension in size])
        )
        image.fill(color=(randint(0, 255), randint(0, 255), randint(0, 255)))
        return image

    def create_rect(self, pos):
        rect = self.image.get_rect()
        rect.topleft = int(pos[0] * scale_factor), int(pos[1] * scale_factor)
        return rect

    def check_mouse_click(self, events: List[Event], mouse):
        mouse_down = pygame.MOUSEBUTTONDOWN in [event.type for event in events]
        if self.rect.collidepoint(mouse):
            self.image
            if mouse_down:
                self.clicked = True
            else:
                self.clicked = False

    def update(self, events, mouse):
        # self.display_surface.blit(self.image, self.rect)
        self.check_mouse_click(events, mouse)
