import pygame
import settings
from presentation.design_elements import Title, Container
from business.entities.player import Player
from presentation.sprite import PlayerSprite


class PlayerStatsContainer:
    """Clase que muestra todas las estadísticas del jugador en un contenedor estilizado."""

    def __init__(self, screen):
        self.screen = screen
        x, y = settings.WORLD_WIDTH//2, settings.WORLD_HEIGHT//2
        self.player = Player(x, y, PlayerSprite(x, y), 100)
        self.screen_width, self.screen_height = settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2
        self.container = Container(0, 100, 400, 700, (0, 0, 100))
        # Configuración del título
        self.title = Title("Estadísticas del Jugador",
                           self.screen_width // 4, 150, 40, (255, 255, 255))

        self.background_color = (30, 30, 30)
        self.text_color = (255, 255, 255)

        self.start_x = 50
        self.start_y = 200
        self.line_spacing = 40

        # Cargar estadísticas del jugador
        self.stats = self.player.json_format()

    def draw_container(self):
        self.container.draw(self.screen)

    def draw_title(self):
        """Dibuja el título 'Estadísticas del Jugador'."""
        self.title.draw(self.screen)

    def draw_stats(self):
        """Dibuja las estadísticas del jugador en pantalla."""
        y_offset = self.start_y
        font = pygame.font.SysFont(None, 30)

        for stat_name, stat_value in self.stats.items():
            text_surface = font.render(f"{stat_name.capitalize()}: {
                                       stat_value}", True, self.text_color)
            self.screen.blit(text_surface, (self.start_x, y_offset))
            y_offset += self.line_spacing

    def draw(self):
        """Dibuja todo el contenedor de estadísticas."""
        self.draw_container()
        self.draw_title()
        self.draw_stats()
        pygame.display.flip()
