"""This module contains interfaces for the game world."""

from abc import ABC, abstractmethod

from business.entities.interfaces import IBullet, IExperienceGem, IMonster, IPlayer


class IGameWorld(ABC):
    """Interface for the game world.

    The game world is the environment in which the game entities exist.
    """

    @abstractmethod
    def add_monster(self, monster: IMonster):
        """Adds a monster to the world.

        Args:
            monster (IMonster): The monster to add.
        """

    @abstractmethod
    def remove_monster(self, monster: IMonster):
        """Removes a monster from the world.

        Args:
            monster (IMonster): The monster to remove.
        """

    @abstractmethod
    def add_experience_gem(self, gem: IExperienceGem):
        """Adds an experience gem to the world.

        Args:
            gem (IExperienceGem): The experience gem to add.
        """

    @abstractmethod
    def remove_experience_gem(self, gem: IExperienceGem):
        """Removes an experience gem from the world.

        Args:
            gem (IExperienceGem): The experience gem to remove.
        """

    @abstractmethod
    def add_bullet(self, bullet: IBullet):
        """Adds a bullet to the world.

        Args:
            bullet (IBullet): The bullet to add.
        """

    @abstractmethod
    def remove_bullet(self, bullet: IBullet):
        """Removes a bullet from the world.

        Args:
            bullet (IBullet): The bullet to remove.
        """

    @abstractmethod
    def update(self):
        """Updates the state of the world and all updatable entities within it."""

    @property
    @abstractmethod
    def player(self) -> IPlayer:
        """Gets the player entity.

        Returns:
            IPlayer: The player entity.
        """

    @property
    @abstractmethod
    def monsters(self) -> list[IMonster]:
        """Gets the list of monsters in the world.

        Returns:
            list[IMonster]: A copy of the list of monsters in the world.
        """

    @property
    @abstractmethod
    def bullets(self) -> list[IBullet]:
        """Gets the list of bullets in the world.

        Returns:
            list[IBullet]: A copy of the list of bullets in the world.
        """

    @property
    @abstractmethod
    def experience_gems(self) -> list[IExperienceGem]:
        """Gets the list of experience gems in the world.

        Returns:
            list[IExperienceGem]: A copy of the list of experience gems in the world.
        """

    @property
    @abstractmethod
    def timer(self) -> int:
        """ Gets the time elapsed (IN-GAME)
        
        Returns:
            int: Number of seconds elapsed in game
        """

    @abstractmethod
    def clear_all_entities(self):
        """Clears all entities from the world."""

    @abstractmethod
    def load_game_data(self, game_data: dict) -> None:
        """ Loads game data

        Args:
            game_data (dict): Json all game data (monsters, bullets, gems, player)
        """

class IUpdatable(ABC):
    """Interface for entities that can be updated."""

    @abstractmethod
    def update(self, world: IGameWorld):
        """Updates the state of the entity.

        Args:
            world (IGameWorld): The game world in which the entity exists.
        """


class IMonsterSpawner(IUpdatable):
    """Interface for a monster spawner.

    A monster spawner is responsible for spawning monsters in the game world.
    """

    @abstractmethod
    def spawn_monster(self, world: IGameWorld):
        """Spawns a monster in the game world.

        Args:
            world (IGameWorld): The game world in which to spawn the monster.
        """


class ITileMap(ABC):
    """Interface for a tile map.

    A tile map is a grid of tiles that make up the game world.
    Each tile has a value that represents the type of terrain or object at that location.
    """

    @abstractmethod
    def get(self, row, col) -> int:
        """Gets the tile at the specified row and column.

        Args:
            row (int): The row of the tile.
            col (int): The column of the tile.

        Returns:
            int: The tile at the specified row and column.
        """
