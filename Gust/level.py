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
    acceleration_up: float = 1
    acceleration_down: float = -1
    velocity: float = 0
    scrolling_damping: float = 0.95

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
        self.rect.bottomleft = (0, screen.get_rect().bottom)


class Wind(Sprite):
    def __init__(self, screen: Surface, dimensions: tuple[int, int]):
        Sprite.__init__(self)

        self.image = pygame.image.load("Assets\\Wind\\Wind.png")
        self.image = pygame.transform.scale(self.image, dimensions)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottomleft = (0, screen.get_rect().bottom)


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

        self.wind_scrolling = ScrollingValues()
        self.wind_scrolling.multiply_attribute("acceleration_up", 2)
        self.wind_scrolling.multiply_attribute("acceleration_down", 2)

        self.background_scrolling = ScrollingValues()

    def scroll_background(self) -> None:
        # scrolling
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.background_scrolling.velocity += (
                self.background_scrolling.acceleration_up
            )
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.background_scrolling.velocity += (
                self.background_scrolling.acceleration_down
            )
        self.background_rect.bottom += int(self.background_scrolling.velocity)

        # keep background in bounds
        if self.background_rect.top > 0:
            self.background_rect.top = 0
        if self.background_rect.bottom < self.screen.get_rect().bottom:
            self.background_rect.bottom = self.screen.get_rect().bottom

        # damping
        self.background_scrolling.velocity *= (
            self.background_scrolling.scrolling_damping
        )

        # draw background
        self.screen.blit(self.background_image, self.background_rect.topleft)

    def scroll_clouds(self) -> None:
        # scrolling
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.cloud_scrolling.velocity += self.cloud_scrolling.acceleration_up
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.cloud_scrolling.velocity += self.cloud_scrolling.acceleration_down
        self.clouds.sprite.rect.bottom += int(self.cloud_scrolling.velocity)

        # keep clouds in bounds
        if self.clouds.sprite.rect.top > 0:
            self.clouds.sprite.rect.top = 0
        if self.clouds.sprite.rect.bottom < self.screen.get_rect().bottom:
            self.clouds.sprite.rect.bottom = self.screen.get_rect().bottom

        # damping
        self.cloud_scrolling.velocity *= self.cloud_scrolling.scrolling_damping

        # draw clouds
        self.clouds.draw(self.screen)

    def scroll_wind(self) -> None:
        # scrolling
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.wind_scrolling.velocity += self.wind_scrolling.acceleration_up
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.wind_scrolling.velocity += self.wind_scrolling.acceleration_down
        self.wind.sprite.rect.bottom += int(self.wind_scrolling.velocity)

        # keep wind in bounds
        if self.wind.sprite.rect.top > 0:
            self.wind.sprite.rect.top = 0
        if self.wind.sprite.rect.bottom < self.screen.get_rect().bottom:
            self.wind.sprite.rect.bottom = self.screen.get_rect().bottom

        # damping
        self.wind_scrolling.velocity *= self.wind_scrolling.scrolling_damping

        # draw wind
        self.wind.draw(self.screen)

    def update_scrolling(self) -> None:
        self.scroll_background()
        self.scroll_clouds()
        self.scroll_wind()

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
