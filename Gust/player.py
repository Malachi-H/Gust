from enum import Enum, auto
import pygame
from pygame.surface import Surface
from pygame.event import Event
from typing import List
from pygame.sprite import Sprite

from screen_dimensions import ScreenDimensions


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()
    STATIONARY = auto()


class Player(Sprite):
    def __init__(
        self, display_surface: Surface, ScreenDimensions: ScreenDimensions
    ) -> None:
        Sprite.__init__(self)

        self.display_surface = display_surface
        self.scale_factor = ScreenDimensions.scale_factor
        self.ACCELERATION_VALUE = 50 * self.scale_factor

        self.image = pygame.Surface((10 * self.scale_factor, 20 * self.scale_factor))
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
        # left keys will be left arrow and a and left mouse down
        left_mouse_button = 1
        right_mouse_buttons = 3
        left_keys = pygame.K_LEFT, pygame.K_a
        right_keys = pygame.K_RIGHT, pygame.K_d
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in left_keys:
                    self.intended_direction = Direction.LEFT
                elif event.key in right_keys:
                    self.intended_direction = Direction.RIGHT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == left_mouse_button:
                    self.intended_direction = Direction.LEFT
                elif event.button == right_mouse_buttons:
                    self.intended_direction = Direction.RIGHT
            if event.type == pygame.KEYUP:
                if event.key in left_keys:
                    self.intended_direction = Direction.RIGHT
                elif event.key in right_keys:
                    self.intended_direction = Direction.LEFT
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == left_mouse_button:
                    self.intended_direction = Direction.RIGHT
                elif event.button == right_mouse_buttons:
                    self.intended_direction = Direction.LEFT

        pressed_keys = pygame.key.get_pressed()
        pressed_mouse_buttons = pygame.mouse.get_pressed()
        left_pressed = False
        right_pressed = False
        for key in left_keys:
            if pressed_keys[key]:
                left_pressed = True
        if pressed_mouse_buttons[
            left_mouse_button - 1
        ]:  # -1 because mouse buttons are 0 indexed
            left_pressed = True
        for key in right_keys:
            if pressed_keys[key]:
                right_pressed = True
        if pressed_mouse_buttons[
            right_mouse_buttons - 1
        ]:  # -1 because mouse buttons are 0 indexed
            right_pressed = True

        if left_pressed and self.intended_direction != Direction.RIGHT:
            if self.velocity.x > 0:
                self.velocity.x = 0
            self.velocity.x += -self.ACCELERATION_VALUE
        elif right_pressed and self.intended_direction != Direction.LEFT:
            if self.velocity.x < 0:
                self.velocity.x = 0
            self.velocity.x += self.ACCELERATION_VALUE

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

    def update(self, events: List[Event], clock) -> None:
        self.get_input(events)
        self.update_position(clock)
        self.draw()
