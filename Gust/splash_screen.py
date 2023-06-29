import pygame
from HelperFunctions import load_full_screen_image
from screen_dimensions import ScreenDimensions
from pygame import Surface

class SplashScreen:
    def __init__(self, screen: Surface, ScreenDimensions: ScreenDimensions):
        self.screen = screen
        self.ScreenDimensions = ScreenDimensions
        self.image = load_full_screen_image(ScreenDimensions, "Assets\\Splash Screen\\splash_screen_high_res.png","Assets\\Splash Screen\\splash_screen.png")
        self.time_after_image_loaded = pygame.time.get_ticks()
        self.stop_displaying = False
        
        
    def update(self):
        self.screen.blit(self.image, (0,0))
        if pygame.time.get_ticks() > 2000 + self.time_after_image_loaded: # 2 seconds
            self.stop_displaying = True
            