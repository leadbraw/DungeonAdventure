import pygame


class Button:
    """Self-explanatory. Used to represent clickable buttons on screen."""

    def __init__(self, color, x, y, width, height, font=None, text_color=None, text=''):
        """Constructor, instantiates fields."""
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.text_color = text_color
        self.text = text

    def draw(self, window, outline=None):
        """
        Draws button on screen.

        :param window: The pygame Surface on which to draw the button.
        :param outline: Whether the button should be drawn with an outline or not. Can be a color or
        boolean. If boolean, defaults to black.
        """
        if outline:
            pygame.draw.rect(window, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)
        # If button has text, draw it!
        if self.text != '':
            text = self.font.render(self.text, True, self.text_color)
            window.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                               self.y + (self.height / 2 - text.get_height() / 2)))

    def is_hovered(self, mouse_pos):
        """
        Returns true if cursor is currently over button, false otherwise.

        :param mouse_pos: The current cursor position (x, y).
        :return: Whether the cursor is currently over the button or not.
        """
        if self.x < mouse_pos[0] < self.x + self.width:
            if self.y < mouse_pos[1] < self.y + self.height:
                return True
        return False
