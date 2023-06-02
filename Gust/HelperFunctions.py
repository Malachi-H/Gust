import pygame
from screen_dimensions import screen_dimensions, scale_factor
from PIL import Image


def load_full_screen_image(path):
    py_image = pygame.image.load(path)
    size = py_image.get_size()
    if size[0] != screen_dimensions[0] or size[1] != screen_dimensions[1]:
        # Resized to display size dimensions
        with Image.open(path) as pil_image:
            rounded_screen_dimensions = tuple(
                [int(screen_dimension) for screen_dimension in screen_dimensions]
            )
            pil_image_resized = pil_image.resize(rounded_screen_dimensions)
            pil_image_resized.save(path)

        # Overwrite with resized image
        py_image = pygame.image.load(path)
    return py_image
