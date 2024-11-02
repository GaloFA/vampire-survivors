"""Player entity module."""

import pygame
import settings
from business.entities.bullet import Bullet
from business.entities.entity import MovableEntity
from business.entities.experience_gem import ExperienceGem
from business.entities.interfaces import ICanDealDamage, IDamageable, IPlayer
from business.world.interfaces import IGameWorld
from presentation.sprite import Sprite


class Player(MovableEntity, IPlayer, IDamageable, ICanDealDamage):
    """Player entity.

    The player is the main character of the game. 
    It can move around the game world and shoot at monsters.
    """

    BASE_DAMAGE = 10
    BASE_SHOOT_COOLDOWN = 100

    def __init__(self, pos_x: int, pos_y: int, sprite: Sprite):
        super().__init__(pos_x, pos_y, 5, sprite)

        self.__health: int = 100
        self.__max_health: int = 100
        self.__last_shot_time = pygame.time.get_ticks()
        self.__experience = 0
        self.__level = 1

    def __str__(self):
        hp = self.__health
        xp = self.__experience
        lvl = self.__level
        pos = str(self._pos_x) + str(self._pos_y)
        return f"Player(hp={hp}, xp={xp}, lvl={lvl}, pos=({pos}))"

    def take_damage(self, amount):
        if not settings.PAUSE:
            self.__health = max(0, self.__health - 0)  # - amount
            self.sprite.take_damage()

    def pickup_gem(self, gem: ExperienceGem):
        if not settings.PAUSE:
            self.__gain_experience(gem.amount)

    def __gain_experience(self, amount: int):
        if not settings.PAUSE:
            self.__experience += amount
            while self.__experience >= self.experience_to_next_level:
                self.__experience -= self.experience_to_next_level
                self.__level += 1

    def __shoot_at_nearest_enemy(self, world: IGameWorld):
        if not settings.PAUSE:
            if not world.monsters:
                return

            monster = min(
                world.monsters,
                key=lambda monster: (
                    (monster.pos_x - self.pos_x) ** 2 +
                    (monster.pos_y - self.pos_y) ** 2
                ),
            )

            bullet = Bullet(self.pos_x, self.pos_y,
                            monster.pos_x, monster.pos_y, 10)
            world.add_bullet(bullet)

    def update(self, world: IGameWorld):
        if not settings.PAUSE:
            super().update(world)

            current_time = pygame.time.get_ticks()
            if current_time - self.__last_shot_time >= self.__shoot_cooldown:
                self.__shoot_at_nearest_enemy(world)
                self.__last_shot_time = current_time

    @property
    def experience(self):
        return self.__experience

    @property
    def experience_to_next_level(self):
        base_xp = 2
        if self.__level == 1:
            return base_xp
        return base_xp * (2 ** (self.__level - 1))

    @property
    def level(self):
        return self.__level

    @property
    def damage_amount(self):
        return Player.BASE_DAMAGE

    @property
    def health(self) -> int:
        return self.__health

    @property
    def max_health(self):
        return self.__max_health

    @property
    def __shoot_cooldown(self):
        return Player.BASE_SHOOT_COOLDOWN
