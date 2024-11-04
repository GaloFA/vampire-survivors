"""Module for the Sprite class."""

import pygame

import settings
from presentation.tileset import Tileset


class Sprite(pygame.sprite.Sprite):
    """A class representing a sprite."""

    def __init__(self, image: pygame.Surface, image_path, rect: pygame.Rect, *groups):
        self._image: pygame.Surface = image
        self._image_path = image_path
        self._rect: pygame.Rect = rect
        super().__init__(*groups)
        self.__is_in_damage_countdown = 0
        self.__original_image: pygame.Surface = image

    @property
    def image(self) -> pygame.Surface:
        """The image of the sprite.

        Returns:
            pygame.Surface: The image of the sprite.
        """
        return self._image

    @property
    def rect(self) -> pygame.Rect:
        """The rect of the sprite.

        Returns:
            pygame.Rect: The rect of the sprite. A rect is a rectangle
            that defines the position and size of the sprite.
        """
        return self._rect

    def update_pos(self, pos_x: float, pos_y: float):
        """Update the position of the sprite.

        Args:
            pos_x (float): The x-coordinate of the sprite.
            pos_y (float): The y-coordinate of the sprite.
        """
        self._rect.center = (int(pos_x), int(pos_y))

    def __restore_image(self):
        self._image = self.__original_image.copy()

    def __change_color(self, color: tuple[int, int, int]):
        self._image = self.__original_image.copy()  # Make a copy of the original image
        # Change color pylint: disable=E1101
        self._image.fill(color, special_flags=pygame.BLEND_MULT)
        self._image.set_colorkey((0, 0, 0))  # Set transparency if necessary

    def __decrease_damage_countdown(self):
        self.__is_in_damage_countdown -= 1
        if self.__is_in_damage_countdown <= 0:
            self.__is_in_damage_countdown = 0
            self.__restore_image()

    def take_damage(self):
        """Take damage."""
        self.__change_color((255, 0, 0))
        self.__is_in_damage_countdown = 30

    def update(self, *args, **kwargs):
        """Update the sprite behavior"""
        super().__init__(*args, **kwargs)
        if self.__is_in_damage_countdown > 0:
            self.__decrease_damage_countdown()

    def serialize_rect(self, rect: pygame.Rect) -> dict:
        """Converts a pygame.Rect object to a dictionary."""
        return {
            'x': rect.x,
            'y': rect.y,
            'width': rect.width,
            'height': rect.height
        }

    def json_format(self):
        return {
            'image_path': self._image_path,
            'rect': self.serialize_rect(self.rect),
            'is_in_damage_countdown': self.__is_in_damage_countdown,
        }


class PlayerSprite(Sprite):
    """A class representing the player sprite."""

    ASSET_IDLE = "./assets/entities/player/player.png"

    TILE_WIDTH = 64
    TILE_HEIGHT = 64
    IDLE_COLUMNS = 4
    RUN_COLUMNS = 6

    def __init__(self, pos_x: float, pos_y: float):
        image: pygame.Surface = pygame.image.load(
            PlayerSprite.ASSET_IDLE).convert_alpha()
        image = pygame.transform.scale(image, settings.TILE_DIMENSION)
        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))

        super().__init__(image, PlayerSprite.ASSET_IDLE, rect)


class ZombieSprite(Sprite):
    """A class representing the zombie sprite."""

    ASSET = "./assets/entities/monsters/zombie/zombie.png"
    TILE_WIDTH = 20
    TILE_HEIGHT = 26
    SIZE_MULTIPLIER = 4

    def __init__(self, pos_x: float, pos_y: float):
        image: pygame.Surface = pygame.image.load(
            ZombieSprite.ASSET).convert_alpha()
        image = pygame.transform.scale(
            image, (ZombieSprite.TILE_WIDTH * ZombieSprite.SIZE_MULTIPLIER, ZombieSprite.TILE_HEIGHT * ZombieSprite.SIZE_MULTIPLIER))
        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))

        super().__init__(image, ZombieSprite.ASSET, rect)


class SkeletonSprite(Sprite):
    """A class representing the skeleton sprite."""

    ASSET = "./assets/entities/monsters/skeleton/skeleton.png"
    TILE_WIDTH = 22
    TILE_HEIGHT = 32
    SIZE_MULTIPLIER = 4

    def __init__(self, pos_x: float, pos_y: float):
        image: pygame.Surface = pygame.image.load(
            SkeletonSprite.ASSET).convert_alpha()
        image = pygame.transform.scale(image, (SkeletonSprite.TILE_WIDTH * SkeletonSprite.SIZE_MULTIPLIER,
                                       SkeletonSprite.TILE_HEIGHT * SkeletonSprite.SIZE_MULTIPLIER))
        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))
        super().__init__(image, SkeletonSprite.ASSET, rect)


class OrcSprite(Sprite):
    """A class representing the orc sprite."""

    ASSET = "./assets/entities/monsters/orc/orc.png"
    TILE_WIDTH = 22
    TILE_HEIGHT = 16
    SIZE_MULTIPLIER = 5

    def __init__(self, pos_x: float, pos_y: float):
        image: pygame.Surface = pygame.image.load(
            OrcSprite.ASSET).convert_alpha()
        image = pygame.transform.scale(
            image, (OrcSprite.TILE_WIDTH * OrcSprite.SIZE_MULTIPLIER, OrcSprite.TILE_HEIGHT * OrcSprite.SIZE_MULTIPLIER))
        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))
        super().__init__(image, OrcSprite.ASSET, rect)


class WerewolfSprite(Sprite):
    """A class representing the werewolf sprite."""

    ASSET = "./assets/entities/monsters/werewolf/werewolf.png"
    TILE_WIDTH = 36
    TILE_HEIGHT = 32
    SIZE_MULTIPLIER = 3

    def __init__(self, pos_x: float, pos_y: float):
        image: pygame.Surface = pygame.image.load(
            WerewolfSprite.ASSET).convert_alpha()
        image = pygame.transform.scale(image, (WerewolfSprite.TILE_WIDTH * WerewolfSprite.SIZE_MULTIPLIER,
                                       WerewolfSprite.TILE_HEIGHT * WerewolfSprite.SIZE_MULTIPLIER))
        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))
        super().__init__(image, WerewolfSprite.ASSET, rect)


class BulletSprite(Sprite):
    """A class representing the bullet sprite."""

    def __init__(self, pos_x: float, pos_y: float):
        image = pygame.Surface(
            (5, 5), pygame.SRCALPHA)  # pylint: disable=E1101
        pygame.draw.circle(image, (255, 255, 0), (2, 2), 5)
        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))

        super().__init__(image, None, rect)


class ExperienceGemSprite(Sprite):
    """A class representing the experience gem sprite."""

    ASSET = "./assets/items/gems/gem.png"
    TILE_WIDTH = 64
    TILE_HEIGHT = 64
    SIZE_MULTIPLIER = 0.75

    def __init__(self, pos_x: float, pos_y: float):
        image: pygame.Surface = pygame.image.load(
            ExperienceGemSprite.ASSET).convert_alpha()
        image = pygame.transform.scale(image, (ExperienceGemSprite.TILE_WIDTH * ExperienceGemSprite.SIZE_MULTIPLIER,
                                       ExperienceGemSprite.TILE_HEIGHT * ExperienceGemSprite.SIZE_MULTIPLIER))
        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))
        super().__init__(image, ExperienceGemSprite.ASSET, rect)


class SpeedGemSprite(Sprite):
    """A class representing the speed gem sprite."""

    ASSET = "./assets/items/gems/gems2/gem1-color5.png"
    TILE_WIDTH = 64
    TILE_HEIGHT = 64
    SIZE_MULTIPLIER = 0.75

    def __init__(self, pos_x: float, pos_y: float):
        image: pygame.Surface = pygame.image.load(
            SpeedGemSprite.ASSET).convert_alpha()
        image = pygame.transform.scale(
            image,
            (
                int(SpeedGemSprite.TILE_WIDTH * SpeedGemSprite.SIZE_MULTIPLIER),
                int(SpeedGemSprite.TILE_HEIGHT * SpeedGemSprite.SIZE_MULTIPLIER)
            )
        )
        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))
        super().__init__(image, SpeedGemSprite.ASSET, rect)


class DamageGemSprite(Sprite):
    """A class representing the damage gem sprite."""

    ASSET = "./assets/items/gems/gems2/triangular2.png"
    TILE_WIDTH = 64
    TILE_HEIGHT = 64
    SIZE_MULTIPLIER = 0.75

    def __init__(self, pos_x: float, pos_y: float):
        image: pygame.Surface = pygame.image.load(
            DamageGemSprite.ASSET).convert_alpha()
        image = pygame.transform.scale(
            image,
            (
                int(DamageGemSprite.TILE_WIDTH *
                    DamageGemSprite.SIZE_MULTIPLIER),
                int(DamageGemSprite.TILE_HEIGHT *
                    DamageGemSprite.SIZE_MULTIPLIER)
            )
        )
        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))
        super().__init__(image, DamageGemSprite.ASSET, rect)


class DefenseGemSprite(Sprite):
    """A class representing the defense gem sprite."""

    ASSET = "./assets/items/gems/gems2/gem11-color6.png"
    TILE_WIDTH = 64
    TILE_HEIGHT = 64
    SIZE_MULTIPLIER = 0.75

    def __init__(self, pos_x: float, pos_y: float):
        image: pygame.Surface = pygame.image.load(
            DefenseGemSprite.ASSET).convert_alpha()
        image = pygame.transform.scale(
            image,
            (
                int(DefenseGemSprite.TILE_WIDTH *
                    DefenseGemSprite.SIZE_MULTIPLIER),
                int(DefenseGemSprite.TILE_HEIGHT *
                    DefenseGemSprite.SIZE_MULTIPLIER)
            )
        )
        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))
        super().__init__(image, DefenseGemSprite.ASSET, rect)
