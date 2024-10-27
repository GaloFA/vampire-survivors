"""This module contains the implementation of the game world."""

from business.entities.interfaces import IBullet, IExperienceGem, IMonster, IPlayer
from business.world.interfaces import IGameWorld, IMonsterSpawner, ITileMap
from business.handlers.cooldown_handler import CooldownHandler
from business.entities.experience_gem import ExperienceGem


class GameWorld(IGameWorld):
    """Represents the game world."""

    def __init__(self, spawner: IMonsterSpawner, tile_map: ITileMap, player: IPlayer):
        # Initialize the player and lists for monsters, bullets and gems
        self.__player: IPlayer = player
        self.__monsters: list[IMonster] = []
        self.__bullets: list[IBullet] = []
        self.__experience_gems: list[IExperienceGem] = []
        self.__spawn_cooldown = CooldownHandler(2500)
        self.__simulation_speed = 1

        # Initialize the tile map
        self.tile_map: ITileMap = tile_map

        # Initialize the monster spawner
        self.__monster_spawner: IMonsterSpawner = spawner

    def update(self):
        self.player.update(self)

        for monster in self.__monsters:
            monster.update(self)

        for bullet in self.__bullets:
            bullet.update(self)

        self.__monster_spawner.update(self)

    def add_monster(self, monster: IMonster):
        if not self.__spawn_cooldown:
            return

        self.__monsters.append(monster)

    def remove_monster(self, monster: IMonster):
        self.__monsters.remove(monster)

        self.add_experience_gem(ExperienceGem(monster.pos_x, monster.pos_y, 1))

    def add_experience_gem(self, gem: IExperienceGem):
        self.__experience_gems.append(gem)

    def remove_experience_gem(self, gem: IExperienceGem):
        self.__experience_gems.remove(gem)

    def add_bullet(self, bullet: IBullet):
        self.__bullets.append(bullet)

    def remove_bullet(self, bullet: IBullet):
        self.__bullets.remove(bullet)

    @property
    def player(self) -> IPlayer:
        return self.__player

    @property
    def monsters(self) -> list[IMonster]:
        return self.__monsters[:]

    @property
    def bullets(self) -> list[IBullet]:
        return self.__bullets[:]

    @property
    def experience_gems(self) -> list[IExperienceGem]:
        return self.__experience_gems[:]

    @property
    def simulation_speed(self) -> int:
        return self.__simulation_speed
