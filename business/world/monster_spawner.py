"""This module contains the MonsterSpawner class."""

import logging
import random
import settings

# import pygame

import settings
from business.entities.monster import Monster
from business.world.interfaces import IGameWorld, IMonsterSpawner
from business.handlers.cooldown_handler import CooldownHandler
from presentation.sprite import MonsterSprite, OrcSprite
from business.world.monster_factory import MonsterFactory

BASE_COOLDOWN = 50


class MonsterSpawner(IMonsterSpawner):
    """Spawns monsters in the game world."""

    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.__spawn_cooldown = CooldownHandler(BASE_COOLDOWN)
        self.__monster_factory = MonsterFactory()

    def update(self, world: IGameWorld):
        #if settings.PAUSE:
        #    return

        if not self.__spawn_cooldown.is_action_ready():
            return

        self.spawn_monster(world)
        self.__spawn_cooldown.put_on_cooldown()

    def spawn_monster(self, world: IGameWorld):
        pos_x = random.randint(0, settings.WORLD_WIDTH)
        pos_y = random.randint(0, settings.WORLD_HEIGHT)

        sprite = MonsterSprite(pos_x, pos_y)

        orc_sprite = OrcSprite(pos_x, pos_y)
        
        orc = self.__monster_factory.create_orc(pos_x, pos_y, orc_sprite)
        
        world.add_monster(orc)
        self.__logger.debug("Spawning Orc at (%d, %d)", pos_x, pos_y)
