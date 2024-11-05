import settings
import pygame
from presentation.design_elements import Title, Button


class GameOverScreen:
    """Clase que representa la pantalla de Game Over con diseño oscuro y misterioso."""

    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT
        self.title = Title("GAME OVER", self.screen_width //
                           2, self.screen_height // 4, 200, (255, 0, 0))

        # Colores y dimensiones de los botones
        button_color = (50, 50, 50)
        button_text_color = (255, 255, 255)
        button_width, button_height = 300, 60

        # Crear botones
        self.restart_button = Button(
            self.screen_width // 2 - button_width // 2,
            self.screen_height // 2,
            button_width,
            button_height,
            "Reiniciar",
            button_color,
            button_text_color
        )
        self.quit_button = Button(
            self.screen_width // 2 - button_width // 2,
            self.screen_height // 2 + 80,
            button_width,
            button_height,
            "Salir",
            button_color,
            button_text_color
        )

    def draw_title(self):
        """Dibuja el título 'Game Over' con un efecto de resplandor."""
        glow_surface = self.title.font.render(
            self.title.text, True, (200, 0, 0))
        glow_rect = glow_surface.get_rect(
            center=(self.title.x, self.title.y))
        self.screen.blit(glow_surface, glow_rect.move(2, 2))  # Resplandor
        self.title.draw(self.screen)

    def draw_buttons(self):
        """Dibuja los botones."""
        self.restart_button.draw(self.screen)
        self.quit_button.draw(self.screen)

    def draw(self):
        """Dibuja toda la pantalla de Game Over."""
        self.screen.fill((62, 62, 62))  # Fondo oscuro
        self.draw_title()
        self.draw_buttons()
        pygame.display.flip()

    def check_click(self, mouse_pos):
        """Verifica si los botones han sido clickeados."""
        if self.restart_button.is_clicked(mouse_pos):
            return 'restart'
        elif self.quit_button.is_clicked(mouse_pos):
            return 'quit'
        return None
