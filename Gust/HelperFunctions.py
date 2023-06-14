import pygame
from screen_dimensions import screen_dimensions, scale_factor
from PIL import Image


def load_full_screen_image(in_path, out_path):
    py_image = pygame.image.load(out_path)
    size = py_image.get_size()
    if size[0] != screen_dimensions[0] or size[1] != screen_dimensions[1]:
        # Resized to display size dimensions
        with Image.open(in_path) as pil_image:
            rounded_screen_dimensions = tuple(
                [int(screen_dimension) for screen_dimension in screen_dimensions]
            )
            pil_image_resized = pil_image.resize(rounded_screen_dimensions)
            pil_image_resized.save(out_path)

        # Overwrite variable with resized image
        py_image = pygame.image.load(out_path)
    return py_image
