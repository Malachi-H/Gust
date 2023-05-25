from typing import List
from pygame.surface import Surface
import pygame
from screen_dimensions import screen_dimensions, scale_factor
from PIL import Image
from pygame.event import Event


class HomeScreen:
    def __init__(self, screen: Surface) -> None:
        self.display_surface = screen
        self.main_screen_gutted = self.load_full_screen_image(
            "Assets\\Main Screen\\main_screen_gutted.png"
        )
        self.level_buttons: pygame.sprite.Group = self.create_level_buttons()

    def update(self, events: List[Event]):
        self.display_surface.blit(self.main_screen_gutted, (0, 0))
        mouse = pygame.mouse.get_pos()
        self.level_buttons.update(events, mouse)
        for button in self.level_buttons:
            if button.clicked:
                print("clicked")

    def load_full_screen_image(self, path):
        py_main_screen_gutted = pygame.image.load(path)
        size = py_main_screen_gutted.get_size()
        if size[0] != screen_dimensions[0] or size[1] != screen_dimensions[1]:
            # Resized to display size dimensions
            with Image.open(path) as pil_main_screen_gutted:
                pil_main_screen_gutted_resized = pil_main_screen_gutted.resize(
                    (screen_dimensions)
                )
                pil_main_screen_gutted_resized.save(
                    "Assets\\Main Screen\\main_screen_gutted.png"
                )

            # Overwrite with resized image
            py_main_screen_gutted = pygame.image.load(path)
        return py_main_screen_gutted

    def create_level_buttons(self):
        buttons = pygame.sprite.Group()
        buttons.add(
            Button(display_surface=self.display_surface, pos=(40, 280), size=(128, 40))
        )
        buttons.add(
            Button(display_surface=self.display_surface, pos=(550, 400), size=(128, 40))
        )
        return buttons


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
        self, display_surface: Surface, pos: tuple[int, int], size: tuple[int, int]
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.display_surface = display_surface
        self.image = pygame.surface.Surface(
            ([dimension * scale_factor for dimension in size])
        )
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.topleft = int(pos[0] * scale_factor), int(pos[1] * scale_factor)

        self.clicked = False

    def check_mouse_click(self, events: List[Event], mouse):
        mouse_down = pygame.MOUSEBUTTONDOWN in [event.type for event in events]
        if self.rect.collidepoint(mouse) and mouse_down:
            self.clicked = True
        else:
            self.clicked = False

    def update(self, events, mouse):
        # self.display_surface.blit(self.image, self.rect)
        self.check_mouse_click(events, mouse)
