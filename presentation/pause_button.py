""" Module that contains representation of buttons in the pause menu. """
import pygame


class Button():
    """Class that represents buttons in the pause menu."""

    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        """Draws the button on the given screen."""
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        """Determines if the button is clicked based on the mouse position."""
        return self.rect.collidepoint(mouse_pos)