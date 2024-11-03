"""This module contains the Monster class, which represents a monster entity in the game."""

import settings
from typing import List

from business.entities.entity import MovableEntity
from business.entities.interfaces import IDamageable, IHasPosition, IHasSprite, IMonster
from business.handlers.cooldown_handler import CooldownHandler
from business.handlers.collision_handler import CollisionHandler
from business.world.interfaces import IGameWorld, IPlayer
from presentation.sprite import Sprite


class Monster(MovableEntity, IMonster):
    """A monster entity in the game."""

    def __init__(self, src_x: int, src_y: int, sprite: Sprite, health: int, max_health: int, damage: int, attack_range: int):
        self.__level_multiplier = 1
        super().__init__(src_x, src_y, 2, sprite)
        self.__health: int = health * self.__level_multiplier
        self.__max_health: int = max_health * self.__level_multiplier
        self.__damage = damage * self.__level_multiplier
        self.__attack_range = attack_range
        self.__attack_cooldown = CooldownHandler(1000)

    def json_format(self):
        return {
            'level_multiplier': self.__level_multiplier,
            'health': self.__health,
            'max_health': self.__max_health,
            'damage': self.__damage,
            'attack_range': self.__attack_range,
            'attack_cooldown': self.__attack_cooldown,
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'sprite': self.sprite,
        }

    def load_monster_from_json(self, monster_data) -> IMonster:
        """Creates a monster from JSON data."""
        src_x = monster_data['pos_x']
        src_y = monster_data['pos_y']
        health = monster_data['health']
        max_health = monster_data['max_health']
        damage = monster_data['damage']
        attack_range = monster_data['attack_range']
        sprite = monster_data['sprite']

        return Monster(src_x, src_y, sprite, health, max_health, damage, attack_range)

    def attack(self, target: IPlayer):
        """Attacks the target."""

        if not self.__attack_cooldown.is_action_ready():
            return

        if self._get_distance_to(target) < self.__attack_range:
            target.take_damage(self.damage_amount)
            self.__attack_cooldown.put_on_cooldown()

    def __get_direction_towards_the_player(self, world: IGameWorld):
        direction_x = world.player.pos_x - self.pos_x
        if direction_x != 0:
            direction_x = direction_x // abs(direction_x)

        direction_y = world.player.pos_y - self.pos_y
        if direction_y != 0:
            direction_y = direction_y // abs(direction_y)

        return direction_x, direction_y

    def levelup(self, world: IGameWorld, levelup_cooldown: CooldownHandler):
        if levelup_cooldown.is_action_ready():
            self.__level_multiplier += (world.timer // 10)

            self.__health *= self.__level_multiplier
            self.__max_health *= self.__level_multiplier
            self.__damage *= self.__level_multiplier

            levelup_cooldown.put_on_cooldown()

    def update(self, world: IGameWorld):

        direction_x, direction_y = self.__get_direction_towards_the_player(
            world)
        
        if (direction_x, direction_y) == (0, 0):
            return

        self.move(direction_x, direction_y)

        if self.__health <= 0:
            world.remove_monster(self)

        self.attack(world.player)

        super().update(world)

    def __str__(self):
        return f"Monster(hp={self.health}, pos={self.pos_x, self.pos_y})"

    def take_damage(self, amount):
        self.__health = max(0, self.__health - amount)
        self.sprite.take_damage()

    @property
    def damage_amount(self):
        return self.__damage

    @property
    def health(self) -> int:
        return self.__health

    @property
    def max_health(self) -> int:
        return self.__max_health
