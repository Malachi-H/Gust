from enum import Enum
import math
from typing import Protocol
from pygame.surface import Surface
import pygame
from player import Player
from pygame.event import Event
from pygame.sprite import Sprite
from pygame.sprite import Group, GroupSingle
from pygame.time import Clock
import scrolling_values



class Clouds(Sprite):
    def __init__(self, screen: Surface, background_dimensions: tuple[int, int]):
        Sprite.__init__(self)

        self.image = pygame.image.load("Assets\\Obstacles\\ObstacleMap.png")
        self.image = pygame.transform.smoothscale(
            self.image, (background_dimensions[0], background_dimensions[1] * 2)
        )
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottomleft = (0, screen.get_rect().bottom)


class Wind(Sprite):
    # * Wind Direction will be stored as a colour value in the texture which is read off to measure the hue and saturation values. The Hue will indicate the direction of the wind as a value between 0 and 1 translating to between 0 and 360 degrees. 0 degrees will equal directly right. 90 degrees (0.25 as hue value) will be directly up. As such the direction will rotate counter-clockwise. The saturation of the colour as a value between 0 and 1 will determine wind speed as a percentage of maximum speed.

    def __init__(self, screen: Surface, background_dimensions: tuple[int, int]):
        Sprite.__init__(self)

        self.image = pygame.image.load("Assets\\Wind\\Wind.png")
        self.image = pygame.transform.smoothscale(
            self.image, (background_dimensions[0], background_dimensions[1] * 2)
        )
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottomleft = (0, screen.get_rect().bottom)


class Background(Sprite):
    def __init__(self, screen: Surface, width: int):
        Sprite.__init__(self)

        self.image = pygame.image.load("Assets\\Background\\BG.png")
        scale_factor = width / self.image.get_rect().width
        dimensions = (
            self.image.get_rect().width * scale_factor,
            self.image.get_rect().height * scale_factor,
        )
        self.image = pygame.transform.scale(self.image, dimensions)
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottomleft = (0, screen.get_rect().bottom)


class Level:
    def __init__(self, screen: Surface):
        self.screen = screen

        # Player
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(screen=self.screen))

        # Background
        self.background = pygame.sprite.GroupSingle()
        self.background.add(
            Background(screen=self.screen, width=self.screen.get_rect().width)
        )

        # Clouds
        self.clouds = pygame.sprite.GroupSingle()
        self.clouds.add(
            Clouds(
                screen=self.screen,
                background_dimensions=self.background.sprite.rect.size,
            )
        )

        # Wind
        self.wind = pygame.sprite.GroupSingle()
        wind = Wind(
            screen=self.screen, background_dimensions=self.background.sprite.rect.size
        )
        self.wind.add(wind)

    def update_scrolling_velocity(self) -> None:
        # apply gravity
        scrolling_values.current_acceleration += scrolling_values.acceleration_gravity
        # apply key input
        if pygame.key.get_pressed()[pygame.K_UP]:
            scrolling_values.current_acceleration += scrolling_values.acceleration_up
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            scrolling_values.current_acceleration += scrolling_values.acceleration_down

        # apply acceleration
        scrolling_values.velocity += scrolling_values.current_acceleration

        # reset acceleration
        scrolling_values.current_acceleration = 0

    def move_layer(self, clock: Clock) -> None:
        # compute new layer position
        self.update_scrolling_velocity()

        # repeat for each layer
        for sprite in [self.background.sprite, self.wind.sprite, self.clouds.sprite]:
            # delta time for frame independence
            dt = clock.get_time() / 1000

            parallax = 1
            if sprite.rect == self.background.sprite.rect:
                parallax = 1
            elif sprite.rect == self.clouds.sprite.rect:
                parallax = 2
            elif sprite.rect == self.wind.sprite.rect:
                parallax = 2

            # move layer
            sprite.position += 0, (scrolling_values.velocity * parallax) * dt
            sprite.rect.center = sprite.position

            # keep layer in bounds
            if sprite.rect.top > 0:
                # set every layer to the top
                for layer in [
                    self.wind.sprite,
                    self.clouds.sprite,
                    self.background.sprite,
                ]:
                    layer.rect.top = 0
                    layer.position = pygame.Vector2(layer.rect.center)

                scrolling_values.velocity = 0
                scrolling_values.current_acceleration = 0
            if sprite.rect.bottom < self.screen.get_rect().bottom:
                # set every layer to the bottom if any layer is above the bottom
                for layer in [
                    self.wind.sprite,
                    self.clouds.sprite,
                    self.background.sprite,
                ]:
                    layer.rect.bottom = self.screen.get_rect().bottom
                    layer.position = pygame.Vector2(layer.rect.center)

                scrolling_values.velocity = 0
                scrolling_values.current_acceleration = 0

            # draw layer
            sprite.rect.center = int(sprite.position.x), int(sprite.position.y)
            self.screen.blit(sprite.image, sprite.rect.topleft)

    def wind_collision(
        self, player_sprite, group: Group | GroupSingle, collide_type
    ) -> None:
        collision = pygame.sprite.spritecollideany(player_sprite, group, collide_type)
        if collision:
            scrolling_values.current_acceleration += scrolling_values.acceleration_up

    def update(self, events: list[Event], clock: Clock) -> None:
        self.move_layer(clock)
        self.player.update(events, clock)
        self.wind_collision(self.player.sprite, self.wind, pygame.sprite.collide_mask)
