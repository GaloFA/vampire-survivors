""" Module that contains respresentation of the pause menu"""
import pygame
from presentation.pause_button import Button
import settings

class PauseMenu:
    def __init__(self, screen):
        """Initializes the PauseMenu object with buttons for resuming and quitting."""
        self.screen = screen
        self.resume_button = Button(200,settings.SCREEN_HEIGHT//2-100 , 200, 50, "Reanudar", (0, 200, 0), (255, 255, 255))
        self.quit_button = Button(200,settings.SCREEN_HEIGHT//2+100, 200, 50, "Salir", (200, 0, 0), (255, 255, 255))
        self.buttons = [self.resume_button, self.quit_button]
        
        self.overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.overlay.set_alpha(128)
        self.overlay.fill((0, 0, 0))

    def draw(self):
        # Dibujar la superposición negra
        self.screen.blit(self.overlay, (0, 0))
        
        # Dibujar los botones
        for button in self.buttons:
            button.draw(self.screen)

    def check_click(self, mouse_pos):
        if self.resume_button.is_clicked(mouse_pos):
            return "resume"
        elif self.quit_button.is_clicked(mouse_pos):
            return "quit"
        return None