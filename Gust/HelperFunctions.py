import pygame
from PIL import Image


def pilImageToSurface(pilImage: Image.Image):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode
    ).convert()
