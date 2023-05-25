from enum import Enum, auto
import pygame
from pygame.surface import Surface
from pygame.event import Event
from typing import List
from pygame.sprite import Sprite

from screen_dimensions import scale_factor


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()
    STATIONARY = auto()


ACCELERATION_VALUE = 50 * scale_factor


class Player(Sprite):
    def __init__(self, display_surface: Surface) -> None:
        Sprite.__init__(self)

        self.display_surface = display_surface
        self.image = pygame.Surface((10 * scale_factor, 20 * scale_factor))
        self.image.fill("orange")
        self.rect = self.image.get_rect()
        self.rect.x = self.display_surface.get_rect().centerx
        self.rect.y = int(self.display_surface.get_rect().height * 0.75)
        self.velocity = pygame.Vector2(0, 0)
        self.intended_direction = Direction.STATIONARY
        self.exact_center = pygame.Vector2(self.rect.center)

    def draw(self) -> None:
        self.display_surface.blit(self.image, self.rect)

    def get_input(self, events: List[Event]) -> None:
        # * Code works but can probably be simplified by tracking most recent key press

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.intended_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.intended_direction = Direction.RIGHT
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.intended_direction = Direction.RIGHT
                elif event.key == pygame.K_RIGHT:
                    self.intended_direction = Direction.LEFT

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.intended_direction != Direction.RIGHT:
            if self.velocity.x > 0:
                self.velocity.x = 0
            self.velocity.x += -ACCELERATION_VALUE
        elif key[pygame.K_RIGHT] and self.intended_direction != Direction.LEFT:
            if self.velocity.x < 0:
                self.velocity.x = 0
            self.velocity.x += ACCELERATION_VALUE

    def update_position(self, clock: pygame.time.Clock) -> None:
        dt = clock.get_time() / 1000
        self.exact_center += (
            self.velocity.x * dt,
            self.velocity.y * dt,
        )
        self.rect.center = int(self.exact_center.x), int(self.exact_center.y)
        # damping / friction
        self.velocity *= 1 - 0.1

    def reset_position(self) -> None:
        self.exact_center.x = self.display_surface.get_rect().centerx
        self.rect.center = int(self.exact_center.x), int(self.exact_center.y)
        self.velocity = pygame.Vector2(0, 0)
        print("reset")

    def update(self, events: List[Event], clock) -> None:
        self.get_input(events)
        self.update_position(clock)
        self.draw()
