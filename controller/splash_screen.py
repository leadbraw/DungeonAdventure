import time
import pygame
from constants import BACKGROUND_COLOR, PASTEL_RED

class SplashScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def display(self, message, setup_function=None, image=None, image_size=None):
        """
        Displays the splash screen with a message and ensures a minimum duration.

        :param message: The message to display on the splash screen.
        :param setup_function: Optional function to run during the splash screen.
        :param image: Optional image to display above the text.
        :param image_size: Tuple (width, height) to resize the image, if provided.
        """
        self.screen.fill(BACKGROUND_COLOR)

        # Display the image if provided
        if image:
            if image_size:
                image = pygame.transform.scale(image, image_size)
            image_x = (self.screen.get_width() - image.get_width()) // 2
            image_y = (self.screen.get_height() // 2) - image.get_height() - 20
            self.screen.blit(image, (image_x, image_y))

        # Render and display the message
        splash_message = self.font.render(message, True, PASTEL_RED)
        text_x = (self.screen.get_width() - splash_message.get_width()) // 2
        text_y = (self.screen.get_height() // 2) + 20
        self.screen.blit(splash_message, (text_x, text_y))

        pygame.display.update()

        # Measure time and run setup function if provided
        start_time = time.time()

        if setup_function:
            setup_function()

        # Ensure splash screen stays for at least 3000ms
        elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        remaining_time = max(0, 3000 - elapsed_time)
        if remaining_time > 0:
            pygame.time.delay(int(remaining_time))