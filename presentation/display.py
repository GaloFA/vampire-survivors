"""Module for displaying the game world."""

import pygame
from game import Game
import settings
from business.world.game_world import GameWorld
from presentation.camera import Camera
from presentation.interfaces import IDisplay
from presentation.tileset import Tileset
from business.entities.interfaces import IMonster


class Display(IDisplay):
    """Class for displaying the game world."""

    def __init__(self):
        # Set the window display mode
        self.__screen = pygame.display.set_mode(settings.SCREEN_DIMENSION)

        # Set the window title
        pygame.display.set_caption(settings.GAME_TITLE)

        # Initialize the camera
        self.camera = Camera()

        self.__ground_tileset = self.__load_ground_tileset()
        self.__world: GameWorld = None # type: ignore

    def __load_ground_tileset(self):
        return Tileset(
            "./assets/ground_tileset.png", settings.TILE_WIDTH, settings.TILE_HEIGHT, 2, 3
        )

    def __render_ground_tiles(self):
        # Calculate the range of tiles to render based on the camera position
        start_col = max(0, self.camera.camera_rect.left // settings.TILE_WIDTH)
        end_col = min(
            settings.WORLD_COLUMNS, (self.camera.camera_rect.right //
                                     settings.TILE_WIDTH) + 1
        )
        start_row = max(0, self.camera.camera_rect.top // settings.TILE_HEIGHT)
        end_row = min(
            settings.WORLD_ROWS, (self.camera.camera_rect.bottom //
                                  settings.TILE_HEIGHT) + 1
        )

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                # Get the tile index from the tile map
                tile_index = self.__world.tile_map.get(row, col)
                tile_image = self.__ground_tileset.get_tile(tile_index)

                # Calculate the position on the screen
                x = col * settings.TILE_WIDTH - self.camera.camera_rect.left
                y = row * settings.TILE_HEIGHT - self.camera.camera_rect.top

                self.__screen.blit(tile_image, (x, y))

    def __draw_player_health_bar(self):
        # Get the player's health
        player = self.__world.player

        # Define the health bar dimensions
        bar_width = settings.SCREEN_WIDTH // 4
        bar_height = 15
        bar_x = settings.SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = settings.SCREEN_HEIGHT - 25

        # Draw the background bar (gray)
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.__screen, (45, 45, 45), bg_rect)

        # Draw the health bar (green)
        health_percentage = player.health / player.max_health
        health_width = int(bar_width * health_percentage)
        health_rect = pygame.Rect(bar_x, bar_y, health_width, bar_height)
        pygame.draw.rect(self.__screen, (0, 255, 0), health_rect)

    def __draw_monster_health_bar(self, monster: IMonster):
        # Get the monster's health
        if monster.health < monster.max_health:
            # Define the health bar dimensions
            bar_width = settings.TILE_WIDTH
            bar_height = 5
            bar_x = monster.sprite.rect.centerx - bar_width // 2 - self.camera.camera_rect.left
            bar_y = monster.sprite.rect.bottom + 5 - self.camera.camera_rect.top

            # Draw the background bar (red)
            bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
            pygame.draw.rect(self.__screen, (255, 0, 0), bg_rect)

            # Draw the health bar (green)
            health_percentage = monster.health / monster.max_health
            health_width = int(bar_width * health_percentage)
            health_rect = pygame.Rect(bar_x, bar_y, health_width, bar_height)
            pygame.draw.rect(self.__screen, (0, 255, 0), health_rect)

    def __draw_player(self):
        adjusted_rect = self.camera.apply(self.__world.player.sprite.rect)
        self.__screen.blit(self.__world.player.sprite.image, adjusted_rect)

        self.__draw_player_health_bar()

        # Draw the experience text
        font = pygame.font.SysFont(None, 30)
        experience_text = font.render(
            f"LEVEL: {self.__world.player.level}",
            True,
            (255, 209, 92),
        )

        # Esto agregue Prueba, Se borra o modifica
        bar_width = settings.SCREEN_WIDTH//2
        bar_height = 10
        xp_ratio = self.__world.player.experience / \
            self.__world.player.experience_to_next_level
        current_xp_width = int(bar_width * xp_ratio)

        pygame.draw.rect(self.__screen, (161, 157, 155), (settings.SCREEN_WIDTH // 4, settings.SCREEN_HEIGHT - 50, bar_width, bar_height))
        pygame.draw.rect(self.__screen, (255, 209, 92), (settings.SCREEN_WIDTH // 4, settings.SCREEN_HEIGHT - 50, current_xp_width, bar_height))

        self.__screen.blit(
            experience_text, (settings.SCREEN_WIDTH//2-45, settings.SCREEN_HEIGHT-80))

    def __draw_timer(self):
        minutes = self.__world.timer // 60
        seconds = self.__world.timer % 60

        timer_text = f"{minutes:02}:{seconds:02}"

        font = pygame.font.SysFont(None, 36)
        timer_surface = font.render(timer_text, True, (255, 255, 255))

        self.__screen.blit(timer_surface, (settings.SCREEN_WIDTH // 2 - 30, 20))

    def load_world(self, world: GameWorld):
        self.__world = world

    def render_frame(self):
        # Update the camera to follow the player
        self.camera.update(self.__world.player.sprite.rect)

        # Render the ground tiles
        self.__render_ground_tiles()

        # Draw all the experience gems
        for gem in self.__world.experience_gems:
            if self.camera.camera_rect.colliderect(gem.sprite.rect):
                adjusted_rect = self.camera.apply(gem.sprite.rect)
                self.__screen.blit(gem.sprite.image, adjusted_rect)

        # Draw all monsters
        for monster in self.__world.monsters:
            if self.camera.camera_rect.colliderect(monster.sprite.rect):
                self.__draw_monster_health_bar(monster)
                adjusted_rect = self.camera.apply(monster.sprite.rect)
                self.__screen.blit(monster.sprite.image, adjusted_rect)

        # Draw the bullets
        for bullet in self.__world.bullets:
            if self.camera.camera_rect.colliderect(bullet.sprite.rect):
                adjusted_rect = self.camera.apply(bullet.sprite.rect)
                self.__screen.blit(bullet.sprite.image, adjusted_rect)

        # Draw the player
        self.__draw_player()

        # Draw timer
        self.__draw_timer()

        # Update the display
        pygame.display.flip()

    @property
    def screen(self):
        return self.__screen
