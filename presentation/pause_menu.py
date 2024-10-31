""" Module that contains respresentation of the pause menu"""
import pygame
from presentation.pause_button import Button


class PauseMenu:
    def __init__(self, screen):
        """Initializes the PauseMenu object with buttons for resuming and quitting."""
        self.screen = screen
        self.resume_button = Button(200, 150, 200, 50, "Reanudar", (0, 200, 0), (255, 255, 255))
        self.quit_button = Button(200, 350, 200, 50, "Salir", (200, 0, 0), (255, 255, 255))
        self.buttons = [self.resume_button, self.quit_button]

    def draw(self):
        for button in self.buttons:
            button.draw(self.screen)

    def check_click(self, mouse_pos):
        if self.resume_button.is_clicked(mouse_pos):
            return "resume"
        elif self.quit_button.is_clicked(mouse_pos):
            return "quit"
        return None
