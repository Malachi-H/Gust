import pygame
from pygame import FULLSCREEN
from pygame.rect import Rect


def wait_for_keypress():
    """ waits for keypress """
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False


def window(game_height):
    """ Creates a square window and draws a square in the top left """
    screen = pygame.display.set_mode((game_height, game_height))
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), Rect(10, 10, 200, 200))
    pygame.display.flip()
    wait_for_keypress()


def fullscreen(game_height):
    """ Sets full screen display mode and draws a square in the top left """
    # game_height = game_width in a square
    screen = pygame.display.set_mode((game_height, game_height), FULLSCREEN)
    screen.fill((255, 255, 255))  # fill white
    pygame.draw.rect(
        screen,  # surface
        (0, 0, 0),  # rgb (black)
        Rect(10, 10, 200, 200))  # (x, y, width, height)
    pygame.display.flip()
    wait_for_keypress()


def fullscreen_fix(game_height):
    """ Sets full screen display mode and draws a square in the top left """
    # Set the display mode to the current screen resolution
    screen = pygame.display.set_mode((0, 0), FULLSCREEN)

    # create a square pygame surface
    game_surface = pygame.Surface((game_height, game_height))
    game_surface.fill((255, 255, 255))

    # draw a square in the top left
    pygame.draw.rect(game_surface, (0, 0, 0), Rect(10, 10, 200, 200))

    # make the largest square surface that will fit on the screen
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    smallest_side = min(screen_width, screen_height)
    screen_surface = pygame.Surface((smallest_side, smallest_side))

    # scale the game surface up to the larger surface
    pygame.transform.scale(
        game_surface,  # surface to be scaled
        (smallest_side, smallest_side),  # scale up to (width, height)
        screen_surface)  # surface that game_surface will be scaled onto

    # place the larger surface in the centre of the screen
    screen.blit(
        screen_surface,
        ((screen_width - smallest_side) // 2,  # x pos
        (screen_height - smallest_side) // 2))  # y pos

    pygame.display.flip()
    wait_for_keypress()


pygame.init()
fullscreen_fix(game_height=1024)