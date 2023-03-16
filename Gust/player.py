from enum import Enum, auto
import pygame
from pygame.surface import Surface
from pygame.event import Event
from typing import List
from pygame.sprite import Sprite
from pygame.sprite import GroupSingle


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()
    STATIONARY = auto()


class Player(Sprite):
    def __init__(self, surface: Surface) -> None:
        Sprite.__init__(self)

        self.image = pygame.Surface((10, 20))
        self.image.fill("orange")
        self.display_surface = surface
        self.position = pygame.Vector2()
        self.position.x = self.display_surface.get_rect().centerx
        self.position.y = self.display_surface.get_rect().height * 0.9
        self.velocity = pygame.Vector2(0, 0)
        self.intended_direction = Direction.STATIONARY

    def draw(self) -> None:
        self.display_surface.blit(self.image, self.position)

    def get_input(self, events: List[Event]) -> None:
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
        if key == pygame.K_LEFT:
            self.intended_direction = key
        if key[pygame.K_LEFT] and self.intended_direction != Direction.RIGHT:
            self.velocity.x += -1
        elif key[pygame.K_RIGHT] and self.intended_direction != Direction.LEFT:
            self.velocity.x += 1

    def update_position(self) -> None:
        self.position += self.velocity
        # damping / friction
        self.velocity *= 0.95

    def check_collision(self, Obstacles: GroupSingle) -> None:
        pass

    def update(self, events: List[Event]) -> None:
        self.get_input(events)
        self.update_position()
        self.draw()
