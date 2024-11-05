"""This module contains interfaces for the entities in the game."""

from abc import ABC, abstractmethod

from presentation.sprite import Sprite


class ICanDealDamage(ABC):
    """Interface for entities that can deal damage."""

    @property
    @abstractmethod
    def damage_amount(self) -> int:
        """The amount of damage the entity can deal.

        Returns:
            int: The amount of damage the entity can deal.
        """


class IDamageable(ABC):
    """Interface for entities that can take damage."""

    @property
    @abstractmethod
    def health(self) -> int:
        """The health of the entity.

        Returns:
            int: The health of the entity.
        """

    @abstractmethod
    def take_damage(self, amount: int):
        """Take damage.

        Args:
            amount (int): The amount of damage to take.
        """


class IUpdatable(ABC):
    """Interface for entities that can be updated."""

    @abstractmethod
    def update(self, world):
        """Update the state of the entity."""


class IHasSprite(ABC):
    """Interface for entities that have a sprite."""

    @property
    @abstractmethod
    def sprite(self) -> Sprite:
        """The sprite of the entity.

        Returns:
            Sprite: The sprite of the entity.
        """


class IHasPosition(IHasSprite):
    """Interface for entities that have a position."""

    @property
    @abstractmethod
    def pos_x(self) -> float:
        """The x-coordinate of the entity.

        Returns:
            float: The x-coordinate of the entity.
        """

    @property
    @abstractmethod
    def pos_y(self) -> float:
        """The y-coordinate of the entity.

        Returns:
            float: The y-coordinate of the entity.
        """


class ICanMove(IHasPosition):
    """Interface for entities that can move."""

    @property
    @abstractmethod
    def speed(self) -> float:
        """The speed of the entity.

        Returns:
            float: The speed of the entity.
        """

    @abstractmethod
    def move(self, direction_x: float, direction_y: float):
        """Move the entity in the given direction based on its speed.

        This method should update the entity's position and sprite.

        Args:
            direction_x (float): The direction in x-coordinate.
            direction_y (float): The direction in y-coordinate.
        """


class IMonster(IUpdatable, ICanMove, IDamageable, ICanDealDamage):
    """Interface for monster entities."""
    @property
    @abstractmethod
    def max_health(self) -> int:
        """The maximum amount of health a player can have.

        Returns:
            int: The max health.
        """

    @property
    @abstractmethod
    def monster_type(self) -> int:
        """The type of the monster.

        Returns:
            str: The type of the monster.
        """

    @abstractmethod
    def levelup(self, world, levelup_cooldown):
        """ Levels up monster every 10 seconds

        Args:
            world (IGameWorld): world instance
            levelup_cooldown (CooldownHandler): cooldown to levelup
        """

    @abstractmethod
    def json_format(self):
        """ Json formatter

        Returns:
            str: json representation of an entity
        """

    @abstractmethod
    def load_monster_from_json(self, monster_data):
        """Creates a monster from JSON data.

        Args:
            monster_data (dict): The data representing the monster.

        Returns:
            IMonster: An instance of a monster.
        """


class IBullet(IUpdatable, ICanMove, IDamageable, ICanDealDamage):
    """Interface for bullet entities."""
    @abstractmethod
    def json_format(self):
        """ Json formatter

        Returns:
            str: json representation of an entity
        """

    @abstractmethod
    def load_bullet_from_json(self, bullet_data):
        """Creates a bullet from JSON data.

        Args:
            bullet_data (dict): The data representing the bullet.

        Returns:
            IBullet: An instance of a bullet.
        """


class IExperienceGem(IUpdatable, IHasPosition):
    """Interface for experience gem entities."""

    @property
    @abstractmethod
    def amount(self) -> int:
        """The amount of experience the gem gives.

        Returns:
            int: The amount of experience the gem gives.
        """
    @abstractmethod
    def load_experience_gem_from_json(self, gem_data):
        """Creates an experience gem from JSON data.

        Args:
            gem_data (dict): The data representing the experience gem.

        Returns:
            IExperienceGem: An instance of an experience gem.
        """

    @abstractmethod
    def json_format(self):
        """ Json formatter

        Returns:
            str: json representation of an entity
        """


class IPlayer(IUpdatable, ICanMove, IDamageable, ICanDealDamage):
    """Interface for the player entity."""

    @abstractmethod
    def pickup_gem(self, gem: IExperienceGem):
        """Picks up an experience gem.

        Args:
            gem (IExperienceGem): The experience gem to pick up.
        """

    @property
    @abstractmethod
    def level(self) -> int:
        """The level of the player.

        Returns:
            int: The level of the player.
        """

    @property
    @abstractmethod
    def experience(self) -> int:
        """The experience of the player.

        Returns:
            int: The experience of the player.
        """

    @property
    @abstractmethod
    def experience_to_next_level(self) -> int:
        """The experience required to reach the next level.

        Returns:
            int: The experience required to reach the next level.
        """

    @property
    @abstractmethod
    def max_health(self) -> int:
        """The maximum amount of health a player can have.

        Returns:
            int: The max health.
        """

    @abstractmethod
    def json_format(self):
        """ Json formatter

        Returns:
            str: json representation of an entity
        """

    @abstractmethod
    def load_player_from_json(self, player_data):
        """Loads the player entity from JSON data.

        Args:
            player_data (dict): The data representing the player.

        Returns:
            IPlayer: An instance of the player.
        """

    @abstractmethod
    def mostrar_estadisticas(self):
        """Muestra las estadísticas del jugador.

        Returns:
            dict: Un diccionario con las estadísticas del jugador, como salud, nivel, experiencia, etc.
        """

    @abstractmethod
    def set_max_health(self, max_health: int):
        """set max health

        Args:
            max_health (int): max health to be added
        """

    @abstractmethod
    def set_speed(self, speed: int):
        """set speed

        Args:
            speed (int): speed to be added
        """

    @abstractmethod
    def set_damage(self, damage: int):
        """set damage

        Args:
            damage (int): damage to be added
        """

    @abstractmethod
    def set_defence(self, defence: int):
        """set defence

        Args:
            defence (int): defence to be added
        """

    @abstractmethod
    def set_experience_mult(self, xp_mult: int):
        """set experience mult

        Args:
            xp_mult (int): xp_mult to be added
        """

    @abstractmethod
    def set_autoheal(self, autoheal: int):
        """set autoheal

        Args:
            autoheal (int): autoheal amount to be added
        """
    @abstractmethod
    def change_weapon(self, direction):
        """Cambia el arma del jugador

        """
