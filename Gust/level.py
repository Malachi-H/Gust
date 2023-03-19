from enum import Enum
from pygame.surface import Surface
import pygame
import struct
from player import Player
from pygame.event import Event
from pygame.sprite import Sprite
from dataclasses import Field, dataclass
from pygame.mask import Mask
from pygame.sprite import Group, GroupSingle
from typing import Literal, List


@dataclass
class ScrollingValues:
    acceleration_gravity = -0.1
    acceleration_up = 1
    acceleration_down = -1
    current_acceleration: float = 0
    velocity: float = 0
    damping: float = 0.05

    def multiply_attribute(self, attribute_name: str, value: float) -> None:
        attribute = getattr(self, attribute_name)
        setattr(self, attribute_name, attribute * value)


class Clouds(Sprite):
    def __init__(self, screen: Surface, dimensions: tuple[int, int]):
        Sprite.__init__(self)

        self.image = pygame.image.load("Assets\\Obstacles\\ObstacleMapV2.png")
        self.image = pygame.transform.scale(self.image, dimensions)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.topleft = (0, 0)


class Wind(Sprite):
    def __init__(self, screen: Surface, dimensions: tuple[int, int]):
        Sprite.__init__(self)

        self.image = pygame.image.load("Assets\\Wind\\Wind.png")
        self.image = pygame.transform.scale(self.image, dimensions)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.topleft = (0, 0)


class Level:
    def __init__(self, screen: Surface):
        self.screen = screen

        # Player
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(surface=self.screen))

        # Background
        self.background_image = pygame.image.load("Assets\Background\BG_V3.png")
        self.background_rect = self.background_image.get_rect()
        self.background_rect.bottomleft = (0, screen.get_rect().bottom)

        # Clouds
        self.clouds = pygame.sprite.GroupSingle()
        clouds = Clouds(screen=self.screen, dimensions=self.background_rect.size)
        self.clouds.add(clouds)

        # Wind
        self.wind = pygame.sprite.GroupSingle()
        wind = Wind(screen=self.screen, dimensions=self.background_rect.size)
        self.wind.add(wind)

        # Scrolling
        self.cloud_scrolling = ScrollingValues()
        self.cloud_scrolling.multiply_attribute("acceleration_up", 2)
        self.cloud_scrolling.multiply_attribute("acceleration_down", 2)
        self.cloud_scrolling.multiply_attribute("acceleration_gravity", 2)
        # self.cloud_scrolling.multiply_attribute("damping", 2)

        self.wind_scrolling = ScrollingValues()
        self.wind_scrolling.multiply_attribute("acceleration_up", 2)
        self.wind_scrolling.multiply_attribute("acceleration_down", 2)
        self.wind_scrolling.multiply_attribute("acceleration_gravity", 2)
        # self.wind_scrolling.multiply_attribute("damping", 2)

        self.background_scrolling = ScrollingValues()

    def move_layer(
        self,
        layer_scrolling: ScrollingValues,
        layer_rect: pygame.Rect,
        layer_image: Surface,
    ) -> None:
        layer_scrolling.current_acceleration = 0
        # apply gravity
        layer_scrolling.current_acceleration += layer_scrolling.acceleration_gravity

        # apply key input
        if pygame.key.get_pressed()[pygame.K_UP]:
            layer_scrolling.current_acceleration += layer_scrolling.acceleration_up
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            layer_scrolling.current_acceleration += layer_scrolling.acceleration_down

        # apply acceleration
        layer_scrolling.velocity += layer_scrolling.current_acceleration

        # apply damping
        layer_scrolling.velocity *= 1 - layer_scrolling.damping

        # move layer
        layer_rect.bottom += int(layer_scrolling.velocity)

        # keep layer in bounds
        if layer_rect.top > 0:
            layer_rect.top = 0
        if layer_rect.bottom < self.screen.get_rect().bottom:
            layer_rect.bottom = self.screen.get_rect().bottom

        # draw layer
        self.screen.blit(layer_image, layer_rect.topleft)

    def update_scrolling(self) -> None:
        wind = [self.wind_scrolling, self.wind.sprite.rect, self.wind.sprite.image]
        cloud = [
            self.cloud_scrolling,
            self.clouds.sprite.rect,
            self.clouds.sprite.image,
        ]
        background = [
            self.background_scrolling,
            self.background_rect,
            self.background_image,
        ]

        for layer_scrolling, layer_rect, layer_image in [background, wind, cloud]:
            self.move_layer(layer_scrolling, layer_rect, layer_image)

    def is_collision(self, sprite, group, collide_type) -> None:
        collision = pygame.sprite.spritecollideany(sprite, group, collide_type)
        return collision

    def update(self, events: list[Event]) -> None:
        self.update_scrolling()
        self.player.update(events)
        collide_cloud = self.is_collision(
            self.player.sprite, self.clouds, pygame.sprite.collide_mask
        )

        collide_wind = self.is_collision(
            self.player.sprite, self.wind, pygame.sprite.collide_mask
        )

        if collide_cloud != None:
            print("collide_cloud")

        if collide_wind != None:
            self.wind_scrolling.velocity += 2
            self.cloud_scrolling.velocity += 2
            self.background_scrolling.velocity += 1
