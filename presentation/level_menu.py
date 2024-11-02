import pygame
# Asegúrate de tener un archivo nivel_button.py que defina la clase Button
from presentation.design_elements import Button, Title, Container, ItemCard
# Archivo donde puedes tener configuraciones como SCREEN_WIDTH y SCREEN_HEIGHT
import settings

width = 1000
height = 100


class NivelMenu:
    def __init__(self, screen):
        """Inicializa el menú de nivelación con opciones y botones para rerollear y skipear."""
        self.screen = screen

        self.container = Container(
            settings.SCREEN_WIDTH//2-300, settings.SCREEN_HEIGHT//2-310, 600, 620, (84, 79, 79))

        self.title1 = Title(
            "¡SUBES DE NIVEL!", settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT-530, 80, (255, 255, 255))
        # Botones de opciones de nivelación

        # Botones de reroll y skip
        self.reroll_button = Button(
            settings.SCREEN_WIDTH-250, settings.SCREEN_HEIGHT // 2 -
            50, 200, 50, "REROLL", (0, 200, 0), (255, 255, 255)
        )
        self.skip_button = Button(
            settings.SCREEN_WIDTH-250, settings.SCREEN_HEIGHT // 2 +
            50, 200, 50, "SKIP", (200, 0, 0), (255, 255, 255)
        )
        self.overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 5))

        self.item_card1 = ItemCard(settings.SCREEN_WIDTH//2-250, settings.SCREEN_HEIGHT//2-125, 500, 100, "Ebony Wings",
                                   "Bombards in a circling zone.", "./assets/experience_gems.png", is_new=True)
        self.item_card2 = ItemCard(settings.SCREEN_WIDTH//2-250, settings.SCREEN_HEIGHT//2, 500, 100, "Ebony Wings",
                                   "Bombards in a circling zone.", "./assets/experience_gems.png", is_new=True)
        self.item_card3 = ItemCard(settings.SCREEN_WIDTH//2-250, settings.SCREEN_HEIGHT//2+125, 500, 100, "Ebony Wings",
                                   "Bombards in a circling zone.", "./assets/experience_gems.png", is_new=True)
        # Lista de botones
        self.buttons = [
            self.reroll_button,
            self.skip_button,
        ]
        self.item_cards = [
            self.item_card1,
            self.item_card2,
            self.item_card3
        ]
        self.containers = [
            self.container
        ]
        self.titles = [self.title1]

    def draw(self):
        """Dibuja el menú de nivelación y sus botones en la pantalla."""
        # Primero, dibuja el fondo negro semi-transparente
        self.screen.blit(self.overlay, (0, 0))

        # Dibujar cada botón
        self.container.draw(self.screen)
        for item in self.item_cards:
            item.draw(self.screen)
        self.title1.draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)

    def check_click(self, mouse_pos):
        """Comprueba si se ha hecho clic en alguno de los botones y devuelve el nombre de la opción."""
        if self.reroll_button.is_clicked(mouse_pos):
            return "reroll"
        elif self.skip_button.is_clicked(mouse_pos):
            return "skip"
        elif self.item_card1.is_clicked(mouse_pos):
            return "item1"
        elif self.item_card1.is_clicked(mouse_pos):
            return "item2"
        elif self.item_card1.is_clicked(mouse_pos):
            return "item3"
        return None
