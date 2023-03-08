from pygame.surface import Surface
import pygame
from player import Player
from pygame.event import Event 





class Level:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.bg_image = pygame.image.load("Assets/BG_V3.png")
        self.ObstacleMap = pygame.image.load("Assets/Obsticles/ObsticleMap.png")
        self.background_rect = self.bg_image.get_rect()
        self.background_rect.bottomleft = (0, screen.get_rect().bottom)
        
        # Player
        self.player = Player(surface = self.screen)

    def update_background(self) -> None:
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.background_rect.bottom += 10
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.background_rect.bottom -= 10

        if self.background_rect.top > 0:
            self.background_rect.top = 0
        if self.background_rect.bottom < self.screen.get_rect().bottom:
            self.background_rect.bottom = self.screen.get_rect().bottom
        self.screen.blit(self.bg_image, self.background_rect.topleft)

    def update(self, events: list[Event]) -> None:
        self.update_background()
        self.player.update(events)
        
