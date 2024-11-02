"""This module defines the Game class."""

import logging
import time
import pygame
import settings
from business.exceptions import DeadPlayerException
from business.handlers.collision_handler import CollisionHandler
from business.handlers.death_handler import DeathHandler
from business.world.interfaces import IGameWorld
from presentation.interfaces import IDisplay, IInputHandler
from presentation.pause_menu import PauseMenu


class Game:
    """
    Main game class.

    This is the game entrypoint.
    """

    def __init__(self, display: IDisplay, game_world: IGameWorld, input_handler: IInputHandler):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__clock = pygame.time.Clock()
        self.__display = display
        self.__world = game_world
        self.__input_handler = input_handler
        self.__running = True
        self.__pause_menu = PauseMenu(display.screen)
        self.__is_paused = False
        self.start_ticks = pygame.time.get_ticks()  # Tiempo de inicio
        self.elapsed_time = 0  # Tiempo transcurrido en segundos

    def __process_game_events(self):
        for event in pygame.event.get():
            # pygame.QUIT event means the user clicked X to close your window
            if event.type == pygame.QUIT:  # pylint: disable=E1101
                self.__logger.debug("QUIT event detected")
                self.__running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.__is_paused = not self.__is_paused

    def run(self):
        """Starts the game loop."""
        self.__logger.debug("Starting the game loop.")
        while self.__running:
            try:
                self.__process_game_events()

                if self.__is_paused:
                    self.__pause_menu.draw()
                    pygame.display.flip()
                    # Detect click in the menu
                    if pygame.mouse.get_pressed()[0]:
                        action = self.__pause_menu.check_click(
                            pygame.mouse.get_pos())
                        if action == "resume":
                            self.__is_paused = False  # Resume the game
                        elif action == "quit":
                            self.__running = False  # Exit the game
                        else:
                            self.__is_paused = False
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
