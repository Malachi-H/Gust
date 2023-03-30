from enum import Enum
import math
from pygame.surface import Surface
import pygame
from player import Player
from pygame.event import Event
from pygame.sprite import Sprite
from pygame.sprite import Group, GroupSingle
from pygame.time import Clock
import scrolling_values


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
        self.background_image = pygame.image.load("Assets\\Background\\BG_V3.png")
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

    def update_scrolling_velocity(self) -> None:
        # apply gravity
        scrolling_values.current_acceleration = scrolling_values.acceleration_gravity

        # apply key input
        if pygame.key.get_pressed()[pygame.K_UP]:
            scrolling_values.current_acceleration += scrolling_values.acceleration_up
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            scrolling_values.current_acceleration += scrolling_values.acceleration_down

        # apply acceleration
        scrolling_values.velocity += scrolling_values.current_acceleration

    def move_layer(self, clock: Clock) -> None:
        # compute new layer position
        self.update_scrolling_velocity()

        wind = [self.wind.sprite.rect, self.wind.sprite.image]
        cloud = [self.clouds.sprite.rect, self.clouds.sprite.image]
        background = [self.background_rect, self.background_image]

        # repeat for each layer
        for layer_rect, layer_image in [background, wind, cloud]:
            # delta time for frame independence
            dt = clock.get_time() / 1000

            parallax = 1
            if layer_rect == self.background_rect:
                parallax = 1
            elif layer_rect == self.clouds.sprite.rect:
                parallax = 2
            elif layer_rect == self.wind.sprite.rect:
                parallax = 2

            # move layer
            layer_rect.bottom += (scrolling_values.velocity * parallax) * dt

            # keep layer in bounds
            if layer_rect.top > 0:
                # set every layer to the top if any layer is above the top
                for rect, _ in [background, wind, cloud]:
                    rect.top = 0
                scrolling_values.velocity = 0
                scrolling_values.current_acceleration = 0
            if layer_rect.bottom < self.screen.get_rect().bottom:
                # set every layer to the bottom if any layer is above the bottom
                for rect, _ in [background, wind, cloud]:
                    rect.bottom = self.screen.get_rect().bottom
                scrolling_values.velocity = 0
                scrolling_values.current_acceleration = 0

            # draw layer
            self.screen.blit(layer_image, layer_rect.topleft)

    def wind_collision(
        self, player_sprite, group: Group | GroupSingle, collide_type
    ) -> None:
        collision = pygame.sprite.spritecollideany(player_sprite, group, collide_type)
        if collision:
            scrolling_values.current_acceleration += scrolling_values.acceleration_up

    def update(self, events: list[Event], clock: Clock) -> None:
        self.move_layer(clock)
        self.player.update(events)
        self.wind_collision(self.player.sprite, self.wind, pygame.sprite.collide_mask)
