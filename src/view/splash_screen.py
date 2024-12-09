import time
import pygame
from constants import BACKGROUND_COLOR, PASTEL_RED


class SplashScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def display(self, message, setup_function=None):
        """
        Displays the splash screen with a message and ensures a minimum duration.

        :param message: The message to display on the splash screen.
        :param setup_function: Optional function to run during the splash screen.
        """
        self.screen.fill(BACKGROUND_COLOR)

        # Render and display the message
        splash_message = self.font.render(message, True, PASTEL_RED)
        text_x = (self.screen.get_width() / 2 - splash_message.get_width() / 2)
        text_y = (self.screen.get_height() / 2 - splash_message.get_height() / 2)
        self.screen.blit(splash_message, (text_x, text_y))

        pygame.display.update()

        # Measure time and run setup function if provided
        start_time = time.time()

        if setup_function:
            setup_function()

        # Ensure splash screen stays for at least 3000ms
        elapsed_time = int(time.time() - start_time) * 1000  # Convert to milliseconds
        remaining_time = max(0, 3000 - elapsed_time)
        if remaining_time > 0:
            pygame.time.delay(int(remaining_time))
