import pygame
from HelperFunctions import load_full_screen_image
from buttons import MouseCollider
from buttons import ButtonType, check_for_and_handle_button_click, Button


class HelpScreen:
    """Handles the visual elements of the help screen and the buttons on it. This includes creating the buttons and responding to button clicks.
    """
    def __init__(self, display_surface, ScreenDimensions):
        self.display_surface = display_surface
        self.ScreenDimensions = ScreenDimensions
        self.help_screen_1 = load_full_screen_image(
            ScreenDimensions,
            "Assets\\Help Screen\\help_screen_1_high_res.png",
            "Assets\\Help Screen\\help_screen_1.png",
        )
        self.help_screen_2 = load_full_screen_image(
            ScreenDimensions,
            "Assets\\Help Screen\\help_screen_2_high_res.png",
            "Assets\\Help Screen\\help_screen_2.png",
        )
        self.current_help_screen = self.help_screen_1
        self.MouseCollider = MouseCollider(
            pygame.mouse.get_pos(), self.display_surface, self.ScreenDimensions
        )
        
        self.help_buttons: pygame.sprite.Group() = self.create_buttons()
        self.button_pressed: (None | ButtonType) = None

    def create_buttons(self):
        buttons = pygame.sprite.Group()
        # Level 1
        buttons.add(
            Button(
                button_type=ButtonType.help_home,
                display_surface=self.display_surface,
                ScreenDimensions=self.ScreenDimensions,
            )
        )
        buttons.add(
            Button(
                button_type=ButtonType.help_next,
                display_surface=self.display_surface,
                ScreenDimensions=self.ScreenDimensions,
            )
        )
        return buttons

    def detect_button_interaction(self, help_buttons, MouseCollider, events):
        for help_button in help_buttons:
            if pygame.sprite.collide_mask(MouseCollider, help_button):
                help_button.image = help_button.image_dict["selected"]
                button_clicks = check_for_and_handle_button_click(events, help_button)
                if button_clicks != None:
                    self.button_pressed = button_clicks
            else:
                help_button.image = help_button.image_dict["unselected"]

    def update(self, events):
        self.display_surface.blit(self.current_help_screen, (0, 0))
        if self.current_help_screen == self.help_screen_1: # conditional statement to only render the next button on the first help screen
            self.help_buttons.update()
        else:
            self.help_buttons.update([ButtonType.help_next])
        self.MouseCollider.update(pygame.mouse.get_pos())
        self.detect_button_interaction(self.help_buttons, self.MouseCollider, events)
