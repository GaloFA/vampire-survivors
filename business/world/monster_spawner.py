"""This module contains the MonsterSpawner class."""

import random
import settings

# import pygame

import settings
from business.entities.monster import Monster
from business.world.interfaces import IGameWorld, IMonsterSpawner
from business.handlers.cooldown_handler import CooldownHandler
from presentation.sprite import ZombieSprite, SkeletonSprite, OrcSprite, WerewolfSprite
from business.entities.monster_factory import MonsterFactory

BASE_COOLDOWN = 800


class MonsterSpawner(IMonsterSpawner):
    """Spawns monsters in the game world."""

    def __init__(self):
        self.__spawn_cooldown = CooldownHandler(BASE_COOLDOWN)
        self.__monster_factory = MonsterFactory()

    def update(self, world: IGameWorld):
        if not self.__spawn_cooldown.is_action_ready():
            return

        self.spawn_monster(world)
        self.__spawn_cooldown.put_on_cooldown()

    def spawn_monster(self, world: IGameWorld):
        pos_x = random.randint(0, settings.WORLD_WIDTH)
        pos_y = random.randint(0, settings.WORLD_HEIGHT)
        monster_type = random.randint(0, 3)

        if monster_type == 0:
            mob_type = "zombie"
            sprite = ZombieSprite(pos_x, pos_y)
            monster = self.__monster_factory.create_monster(pos_x, pos_y, sprite, mob_type)
        if monster_type == 1:
            mob_type = "skeleton"
            sprite = SkeletonSprite(pos_x, pos_y)
            monster = self.__monster_factory.create_monster(pos_x, pos_y, sprite, mob_type)
        if monster_type == 2:
            mob_type = "orc"
            sprite = OrcSprite(pos_x, pos_y)
            monster = self.__monster_factory.create_monster(pos_x, pos_y, sprite, mob_type)
        if monster_type == 3:
            mob_type = "werewolf"
            sprite = WerewolfSprite(pos_x, pos_y)
            monster = self.__monster_factory.create_monster(pos_x, pos_y, sprite, mob_type)

        world.add_monster(monster)
