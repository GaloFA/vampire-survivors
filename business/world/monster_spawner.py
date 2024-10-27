"""This module contains the MonsterSpawner class."""

import logging
import random

#import pygame

import settings
from business.entities.monster import Monster
from business.world.interfaces import IGameWorld, IMonsterSpawner
from business.handlers.cooldown_handler import CooldownHandler
from presentation.sprite import MonsterSprite

BASE_COOLDOWN = 400
class MonsterSpawner(IMonsterSpawner):
    """Spawns monsters in the game world."""

    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.__spawn_cooldown = CooldownHandler(BASE_COOLDOWN)

    def update(self, world: IGameWorld):
        if not self.__spawn_cooldown.is_action_ready() or world.simulation_speed != 1:
            return

        self.spawn_monster(world)
        self.__spawn_cooldown.put_on_cooldown()

    def spawn_monster(self, world: IGameWorld):
        pos_x = random.randint(0, settings.WORLD_WIDTH)
        pos_y = random.randint(0, settings.WORLD_HEIGHT)
        monster = Monster(pos_x, pos_y, MonsterSprite(pos_x, pos_y))
        world.add_monster(monster)
        self.__logger.debug("Spawning monster at (%d, %d)", pos_x, pos_y)
