from time import sleep
from pygame.surface import Surface
import pygame
from player import Player
from pygame.event import Event
from pygame.sprite import Sprite
from pygame.sprite import Group, GroupSingle
from pygame.time import Clock
import scrolling_values
from screen_dimensions import ScreenDimensions
from HelperFunctions import load_full_screen_image


class Level:
    """Handles the elements interacting on the level screen. This includes the player, background, clouds, wind, and level complete text. This class also handles the parallax scrolling of the background, clouds, and wind."""

    def __init__(self, screen: Surface, ScreenDimensions: ScreenDimensions):
        self.screen = screen
        self.ScreenDimensions = ScreenDimensions

        # Player
        self.player = pygame.sprite.GroupSingle()
        self.player.add(
            Player(display_surface=self.screen, ScreenDimensions=ScreenDimensions)
        )

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

        # Level Complete Text
        self.level_complete_img = load_full_screen_image(
            self.ScreenDimensions,
            "Assets\\Win Screen\\win_screen_high_res.png",
            "Assets\\Win Screen\\win_screen.png",
        )
        self.level_complete = False

    def update_scrolling_velocity(self) -> None:
        """Handles the calculations for how much to move each layer"""
        # apply gravity
        scrolling_values.current_acceleration += scrolling_values.acceleration_gravity
        # apply key input
        up_keys = pygame.K_UP, pygame.K_w
        down_keys = pygame.K_DOWN, pygame.K_s
        up_key_pressed = False
        down_key_pressed = False
        for key in up_keys:
            if pygame.key.get_pressed()[key]:
                up_key_pressed = True
        for key in down_keys:
            if pygame.key.get_pressed()[key]:
                down_key_pressed = True

        if up_key_pressed:
            scrolling_values.current_acceleration += scrolling_values.acceleration_up
        if down_key_pressed:
            scrolling_values.current_acceleration += scrolling_values.acceleration_down

        # apply acceleration
        scrolling_values.velocity += scrolling_values.current_acceleration

        # reset acceleration
        scrolling_values.current_acceleration = 0

    def move_and_draw_layer(self, clock: Clock) -> None:
        """handles the movement and drawing of the background, clouds, and wind layers."""
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
            sprite.position += (
                0,
                (scrolling_values.velocity * parallax)
                * dt
                * self.ScreenDimensions.scale_factor,
            )
            sprite.rect.center = sprite.position

            # keep layer in bounds
            if sprite.rect.top > 0:
                self.level_complete = True

            if sprite.rect.bottom <= self.screen.get_rect().bottom:
                # set every layer to the bottom if any layer is above the bottom
                for layer in [
                    self.wind.sprite,
                    self.clouds.sprite,
                    self.background.sprite,
                ]:
                    layer.rect.bottom = (
                        self.screen.get_rect().bottom + 1
                    )  # +1 to prevent layer staying stuck at the bottom of screen due to velocity being reset to 0 when player lands on the ground.
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

    def obstacle_collision(
        self, player_sprite, group: Group | GroupSingle, collide_type
    ) -> None:
        collision = pygame.sprite.spritecollideany(player_sprite, group, collide_type)
        if collision:
            scrolling_values.current_acceleration = 0
            sleep(0.5)
            self.restart_level()

    def restart_level(self):
        scrolling_values.velocity = 0
        self.player.sprite.reset_position()
        for sprite in [
            self.wind.sprite,
            self.clouds.sprite,
            self.background.sprite,
        ]:
            sprite.rect.bottom = self.screen.get_rect().bottom
            sprite.position = pygame.Vector2(sprite.rect.center)

    def update(self, events: list[Event], clock: Clock) -> None:
        self.move_and_draw_layer(clock)
        self.player.update(events, clock)
        self.wind_collision(self.player.sprite, self.wind, pygame.sprite.collide_mask)
        self.obstacle_collision(
            self.player.sprite, self.clouds, pygame.sprite.collide_mask
        )
        if self.level_complete == True:
            self.screen.blit(self.level_complete_img, (0, 0))


class Background(Sprite):
    """Sprite class to handle the background layer of the game."""

    def __init__(self, screen: Surface, width: int):
        Sprite.__init__(self)

        self.image = pygame.image.load("Assets\\Background\\BG.png")
        img_scale_factor = width / self.image.get_rect().width
        dimensions = (
            self.image.get_rect().width * img_scale_factor,
            self.image.get_rect().height * img_scale_factor,
        )
        self.image = pygame.transform.scale(self.image, dimensions)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = screen.get_rect().bottomleft
        self.position = pygame.Vector2(self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)


class Clouds(Sprite):
    """Sprite class to handle the clouds layer of the game."""

    def __init__(self, screen: Surface, background_dimensions: tuple[int, int]):
        Sprite.__init__(self)

        self.image = pygame.image.load("Assets\\Obstacles\\ObstacleMap.png")
        self.image = pygame.transform.smoothscale(
            self.image,
            (
                background_dimensions[0],
                background_dimensions[1] * 2 - screen.get_height(),
            ),
        )
        self.rect = self.image.get_rect()
        self.rect.bottomleft = screen.get_rect().bottomleft
        self.position = pygame.Vector2(self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)


class Wind(Sprite):
    """Sprite class to handle the wind layer of the game."""

    def __init__(self, screen: Surface, background_dimensions: tuple[int, int]):
        Sprite.__init__(self)

        self.image = pygame.image.load("Assets\\Wind\\Wind.png")
        self.image = pygame.transform.smoothscale(
            self.image,
            (
                background_dimensions[0],
                background_dimensions[1] * 2 - screen.get_height(),
            ),
        )
        self.rect = self.image.get_rect()
        self.rect.bottomleft = screen.get_rect().bottomleft
        self.position = pygame.Vector2(self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
