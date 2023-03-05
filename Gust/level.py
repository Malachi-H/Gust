from pygame.surface import Surface
import pygame
from pygame.sprite import Sprite


def convert_imageMap_to_entities(imageMap: Surface) -> list[Sprite]:
    """Converts an image map to a list of entities.

    Args:
        imageMap (Surface): The image map to convert.

    Returns:
        list[Surface]: A list of entities.
    """
    entities = []
    for y in range(imageMap.get_height()):
        for x in range(imageMap.get_width()):
            if imageMap.get_at((x, y)) != (0, 0, 0, 0):
                entity = pygame.sprite.Sprite()
                entity.image = pygame.Surface((1, 1))
                entity.image.fill(imageMap.get_at((x, y)))
                entity.rect = entity.image.get_rect()
                entity.rect.topleft = (x, y)
                entities.append(entity)
    return entities


class Level:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.bg_image = pygame.image.load("Assets/BG_V3.png")
        self.ObstacleMap = pygame.image.load("Assets/Obsticles/ObsticleMap.png")
        self.background_rect = self.bg_image.get_rect()
        self.background_rect.bottomleft = (0, screen.get_rect().bottom)
        obstacles = convert_imageMap_to_entities(self.ObstacleMap)
        self.obstacles = pygame.sprite.Group(*obstacles)

    def update_background(self) -> None:
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.background_rect.bottom += 10
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.background_rect.bottom -= 10

        if self.background_rect.top > 0:
            self.background_rect.top = 0
        if self.background_rect.bottom < self.screen.get_rect().bottom:
            self.background_rect.bottom = self.screen.get_rect().bottom
        self.screen.blit(self.bg_image, self.background_rect.topleft)

    def update(self) -> None:
        self.update_background()
        pygame.sprite.Group.draw(self.obstacles, self.screen)
