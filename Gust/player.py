from enum import Enum, auto
import pygame
from pygame.surface import Surface
from pygame.event import Event
from typing import List
from pygame.sprite import Sprite


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()
    STATIONARY = auto()


ACCELERATION_VALUE = 0.2


class Player(Sprite):
    def __init__(self, surface: Surface) -> None:
        Sprite.__init__(self)

        self.image = pygame.Surface((10, 20))
        self.image.fill("orange")
        self.display_surface = surface
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

    def update_position(self) -> None:
        self.exact_center += self.velocity.x, self.velocity.y
        self.rect.center = int(self.exact_center.x), int(self.exact_center.y)
        self.rect.y += int(self.velocity.y)
        # damping / friction
        self.velocity *= 0.98

    def update(self, events: List[Event]) -> None:
        self.get_input(events)
        self.update_position()
        self.draw()
