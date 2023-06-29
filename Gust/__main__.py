import pygame
from screen_dimensions import ScreenDimensions
from window import Window


class Game:
    """Base class for the game. This class is responsible for creating the window and running the game loop. It is also responsible for re-initialising the window when the resolution is changed
    """
    def __init__(self) -> None:
        pygame.init()
        self._is_first_start_up = True
        self.ScreenDimensions = ScreenDimensions()
        self.window = Window(self.ScreenDimensions, self._is_first_start_up)
        self.clock = pygame.time.Clock()

    @property
    def is_first_start_up(self) -> bool:
        """determines if the window is being run for the first time by checking the windows is_first_start_up property. This is used to determine if the splash screen should be displayed or not

        Returns:
            bool: True if window is being loaded for the first time, False otherwise
        """
        self._is_first_start_up = self.window.is_first_start_up
        return self._is_first_start_up

    def make_window(self):
        return Window(self.ScreenDimensions, self.is_first_start_up)

    def run(self):
        active = True
        while active:
            # pump = False augment is broken so event.get() can only be used once per frame with the lines result passed to other files
            events = pygame.event.get()
            for event in events:
                if (  # Conditions for closing the application: pressing the x button or pressing ctrl + q
                    event.type == pygame.QUIT
                    or pygame.key.get_pressed()[pygame.K_LCTRL]
                    and pygame.key.get_pressed()[pygame.K_q]
                    or pygame.key.get_pressed()[pygame.K_RCTRL]
                    and pygame.key.get_pressed()[pygame.K_q]
                ):
                    active = False

            self.window.update(events, self.clock)
            if self.window.restart_screen == True:
                pygame.display.quit()
                pygame.display.init()
                self.window = self.make_window()
            pygame.display.update()
            self.clock.tick(60)


game = Game()
game.run()
