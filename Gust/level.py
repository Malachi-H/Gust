from enum import Enum
from pygame.surface import Surface
import pygame
import struct
from player import Player
from pygame.event import Event
from pygame.sprite import Sprite
from dataclasses import dataclass


@dataclass
class ScrollingVariables:
    acceleration_up: float = 1
    acceleration_down: float = -1
    velocity: float = 0
    scrolling_damping: float = 0.95


class Clouds(Sprite):
    def __init__(self, screen: Surface, dimensions: tuple[int, int]):
        Sprite.__init__(self)

        self.image = pygame.image.load("Assets\\Obstacles\\ObstacleMapV2.png")
        self.image = pygame.transform.scale(self.image, dimensions)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottomleft = (0, screen.get_rect().bottom)


class Level:
    def __init__(self, screen: Surface):
        self.screen = screen

        # Player
        self.player = Player(surface=self.screen)

        # Background
        self.background_image = pygame.image.load("Assets/BG_V3.png")
        self.background_rect = self.background_image.get_rect()
        self.background_rect.bottomleft = (0, screen.get_rect().bottom)

        # Clouds
        self.clouds = pygame.sprite.GroupSingle()
        clouds = Clouds(screen=self.screen, dimensions=self.background_rect.size)
        self.clouds.add(clouds)

        # Scrolling
        self.cloud_scrolling = ScrollingVariables(acceleration_up=2, acceleration_down=-2)
        self.background_scrolling = ScrollingVariables()

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

        # draw clouds
        self.clouds.draw(self.screen)

    def update_scrolling(self) -> None:
        self.scroll_background()
        self.scroll_clouds()

        self.cloud_scrolling.velocity *= self.cloud_scrolling.scrolling_damping
        self.background_scrolling.velocity *= (
            self.background_scrolling.scrolling_damping
        )

    def update(self, events: list[Event]) -> None:
        self.update_scrolling()
        self.player.update(events)
        self.player.check_collision(self.clouds)
