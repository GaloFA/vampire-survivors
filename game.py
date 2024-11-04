"""This module defines the Game class."""

import pygame
import settings
from business.exceptions import DeadPlayerException
from business.handlers.collision_handler import CollisionHandler
from business.handlers.death_handler import DeathHandler
from business.world.interfaces import IGameWorld
from presentation.interfaces import IDisplay, IInputHandler
from presentation.pause_menu import PauseMenu
from presentation.level_menu import NivelMenu
from presentation.game_over_screen import GameOverScreen
from presentation.player_stats import PlayerStatsContainer
from business.entities.player import Player
from business.entities.items import DiccionarioClass
from persistence.gamejsondao import GameWorldJsonDAO


class Game:
    """
    Main game class.

    This is the game entrypoint.
    """

    def __init__(self, display: IDisplay, game_world: IGameWorld, input_handler: IInputHandler, restart_game_func):
        self.__clock = pygame.time.Clock()
        self.__display = display
        self.__world = game_world
        self.__input_handler = input_handler
        self.__running = True
        self.__player_stats = PlayerStatsContainer(
            display.screen, self.__world.player.mostrar_estadisticas())
        self.__pause_menu = PauseMenu(display.screen)
        self.__level_menu = NivelMenu(display.screen)
        self.__game_over = GameOverScreen(display.screen)
        self.__items_inicializados = False
        self.__is_game_over = False
        self.__is_paused = False
        self.__is_level_up_menu_active = False
        self.start_ticks = pygame.time.get_ticks()  # Tiempo de inicio
        self.elapsed_time = 0  # Tiempo transcurrido en segundos
        self.previous_level = self.__world.player.level
        self.__dao = GameWorldJsonDAO()
        self.__loaded: bool = False
        self.__restart_game_func = restart_game_func

    def __process_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=E1101
                self.__running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.__is_paused = not self.__is_paused

    def save_game(self):
        """Saves the current game state using the DAO."""
        self.__dao.save_game(self.__world)

    def load_game(self):
        """Loads the game state using the DAO."""
        self.__dao.load_game(self.__world)

    def __handle_game_over_screen(self):
        self.__game_over.draw()
        pygame.display.flip()

        if pygame.mouse.get_pressed()[0]:
            action = self.__game_over.check_click(
                pygame.mouse.get_pos())
            if action == 'restart':
                self.__restart_game()
            if action == 'quit':
                self.__running = False

    def __handle_pause_menu(self):
        self.__pause_menu.draw()
        self.__player_stats.draw()
        pygame.display.flip()

        if pygame.mouse.get_pressed()[0]:
            keys = pygame.key.get_pressed()
            action = self.__pause_menu.check_click(pygame.mouse.get_pos())
            if action == "r":
                self.__is_paused = False

            elif action == "q":
                self.__running = False
            elif action == "sq":
                self.save_game()
                self.__running = False

            elif keys[pygame.K_ESCAPE]:
                self.__is_paused = False

    def __handle_level_up_menu(self):
        if not self.__items_inicializados:
            self.initialize_items()

        if pygame.mouse.get_pressed()[0]:
            action = self.__level_menu.check_click(
                pygame.mouse.get_pos())

            if isinstance(action, str):
                if action == "skip":
                    self.__items_inicializados = False
                    self.__is_level_up_menu_active = False
                if action == "reroll":
                    self.reroll_items()

            else:
                #  item_selecionado= action
                #    item_selecionado.
                self.__items_inicializados = False
            if action == "item2":
                self.__items_inicializados = False
            if action == "item3":
                self.__items_inicializados = False
            if action == "skip":
                self.__items_inicializados = False
            if action == "reroll":
                self.reroll_items()
            self.__is_level_up_menu_active = False

    def initialize_items(self):
        Diccionario_Clases = DiccionarioClass()
        diccionario_items = Diccionario_Clases.select_random_items()
        item_cards = self.__level_menu.colocar_items(diccionario_items)
        self.__level_menu.draw(item_cards)
        self.__player_stats.draw()
        pygame.display.flip()
        self.__items_inicializados = True  # Marcar como inicializado
        return diccionario_items

    def reroll_items(self):
        self.__items_inicializados = False

    def __restart_game(self):
        self.__restart_game_func()

    def run(self):
        """Starts the game loop."""
        while self.__running:
            if self.__dao.has_saved_game_data() and not self.__loaded:
                self.__loaded = True
                self.__dao.load_game(self.__world)
            try:
                self.__process_game_events()

                if self.__is_paused:
                    self.__handle_pause_menu()
                    continue

                current_level = self.__world.player.level
                if current_level > self.previous_level:
                    self.__is_level_up_menu_active = True
                    self.previous_level = current_level

                if self.__is_level_up_menu_active:
                    self.__handle_level_up_menu()
                    continue
                if self.__world.player.health <= 0:
                    self.__is_game_over = True

                if self.__is_game_over:
                    self.__handle_game_over_screen()
                    self.__dao.clear_save()
                    continue

                self.elapsed_time = (
                    pygame.time.get_ticks() - self.start_ticks) / 1000
                self.__input_handler.process_input()
                self.__world.update()
                CollisionHandler.handle_collisions(self.__world)
                DeathHandler.check_deaths(self.__world)
                self.__display.render_frame()

                self.__clock.tick(settings.FPS)
            except DeadPlayerException:
                self.__running = False
