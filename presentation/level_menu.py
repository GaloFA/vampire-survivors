import pygame
from presentation.design_elements import Button, Title, Container, ItemCard
import settings
from business.entities.items import *
from business.world.interfaces import IGameWorld


class NivelMenu:
    def __init__(self, screen, game_world: IGameWorld):
        """Inicializa el menú de nivelación con opciones y botones para rerollear y skipear."""
        self.screen = screen
        self.game_world = game_world
        button_color = (50, 50, 50)
        button_text_color = (255, 255, 255)
        self.container = Container(
            settings.SCREEN_WIDTH//2-300, settings.SCREEN_HEIGHT//2-310, 600, 620, (84, 79, 79))

        self.title1 = Title(
            "SUBES DE NIVEL", settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2-210, 80, (255, 255, 255))
        # Botones de opciones de nivelación

        # Botones de reroll y skip
        self.reroll_button = Button(
            settings.SCREEN_WIDTH-250, settings.SCREEN_HEIGHT // 2 -
            50, 200, 50, "REROLL", button_color, button_text_color
        )
        self.skip_button = Button(
            settings.SCREEN_WIDTH-250, settings.SCREEN_HEIGHT // 2 +
            50, 200, 50, "SKIP", button_color, button_text_color
        )

        self.item_card1 = ItemCard(settings.SCREEN_WIDTH//2-250, settings.SCREEN_HEIGHT//2-125, 500, 100, "Ebony Wings",
                                   "Bombards in a circling zone.", "./assets/items/gems/health_gem.png", is_new=True)
        self.item_card2 = ItemCard(settings.SCREEN_WIDTH//2-250, settings.SCREEN_HEIGHT//2, 500, 100, "Ebony Wings",
                                   "Bombards in a circling zone.", "./assets/items/gems/health_gem.png", is_new=True)
        self.item_card3 = ItemCard(settings.SCREEN_WIDTH//2-250, settings.SCREEN_HEIGHT//2+125, 500, 100, "Ebony Wings",
                                   "Bombards in a circling zone.", "./assets/items/gems/health_gem.png", is_new=True)
        self.overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill((42, 42, 42))

        # Lista de botones
        self.buttons = [
            self.reroll_button,
            self.skip_button,
        ]
        self.items_dict = {}
        self.items_card = {}

    # SE ENCARGA DE RECIBIR EL DICCIONARIO CON LOS 3 ITEMS ELEGIDOS Y REMPLAZA TODA LA INFO DE ESTOS EN LA ITEM_CARD

    def colocar_items(self, items: dict):
        """Coloca los ítems en el menú de nivelación y actualiza las ItemCards."""
        posiciones = [
            (settings.SCREEN_WIDTH // 2 - 250, settings.SCREEN_HEIGHT // 2 - 125),
            (settings.SCREEN_WIDTH // 2 - 250, settings.SCREEN_HEIGHT // 2),
            (settings.SCREEN_WIDTH // 2 - 250, settings.SCREEN_HEIGHT // 2 + 125)
        ]

        # Asignar cada ítem del diccionario a una ItemCard
        for index, (key, item) in enumerate(items.items()):
            if index < 3:
                x, y = posiciones[index]
                if item:  # Verificar que el ítem no sea None
                    item_card = ItemCard(
                        x, y, 500, 100, item._name, item._description, item._image_path, is_new=True
                    )
                    # Guardar la ItemCard en el diccionario
                    self.items_card[key] = item_card
                    self.items_dict[key] = item

            print(self.items_dict)

        return self.items_dict

    def draw(self, item_cards):
        """Dibuja el menú de nivelación y sus botones en la pantalla."""
        self.screen.blit(self.overlay, (0, 0))

        self.container.draw(self.screen)
        self.title1.draw(self.screen)
        # Dibuja cada ItemCard en el diccionario
        for item_display in self.items_card.values():
            item_display.draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)

    def check_click(self, mouse_pos):
        """Comprueba si se ha hecho clic en alguno de los botones y devuelve el nombre de la opción."""
        if self.reroll_button.is_clicked(mouse_pos):
            return "reroll"
        elif self.skip_button.is_clicked(mouse_pos):
            return "skip"
        elif self.item_card1.is_clicked(mouse_pos):
            item_key = list(self.items_dict.keys())[0]
            self.items_dict[item_key].apply_effect(self.game_world.player)
            self.items_dict = {}
            return 'item1'

        elif self.item_card2.is_clicked(mouse_pos):
            item_key = list(self.items_dict.keys())[1]
            self.items_dict[item_key].apply_effect(self.game_world.player)
            self.items_dict = {}
            return 'item2'
        elif self.item_card3.is_clicked(mouse_pos):
            item_key = list(self.items_dict.keys())[2]
            self.items_dict[item_key].apply_effect(self.game_world.player)
            self.items_dict = {}
            return 'item3'
        return None
