"""This module contains the implementation of the game world."""
import random
from business.entities.interfaces import IBullet, IExperienceGem, IMonster, IPlayer
from business.world.interfaces import IGameWorld, IMonsterSpawner, ITileMap
from business.handlers.cooldown_handler import CooldownHandler
from business.entities.experience_gem import *
from business.entities.monster import Monster
from business.entities.bullet import Bullet
from business.entities.player import Player


class GameWorld(IGameWorld):
    """Represents the game world."""

    def __init__(self, spawner: IMonsterSpawner, tile_map: ITileMap, player: IPlayer):
        # Initialize the player and lists for monsters, bullets and gems
        self.__player: IPlayer = player
        self.__monsters: list[IMonster] = []
        self.__bullets: list[IBullet] = []
        self.__experience_gems: list[IExperienceGem] = []
        self.__spawn_cooldown = CooldownHandler(2500)
        self.__monster_levelup_cooldown = CooldownHandler(10000)

        # Initialize the tile map
        self.tile_map: ITileMap = tile_map

        # Initialize the monster spawner
        self.__monster_spawner: IMonsterSpawner = spawner

        # Timer
        self.__timer = 0
        self.__timer_cooldown = CooldownHandler(1000)

    def update(self):
        self.player.update(self)

        for monster in self.__monsters:
            monster.update(self)
            monster.levelup(self, self.__monster_levelup_cooldown)

        for bullet in self.__bullets:
            bullet.update(self)

        self.__monster_spawner.update(self)

        if self.__timer_cooldown.is_action_ready():
            self.__timer += 1
            self.__timer_cooldown.put_on_cooldown()

    def add_monster(self, monster: IMonster):
        if not self.__spawn_cooldown:
            return

        self.__monsters.append(monster)

    def remove_monster(self, monster: IMonster):
        self.__monsters.remove(monster)

        # Genera un número aleatorio entre 0 y 100
        probability = random.uniform(0, 100)
        if probability <= 20:
            pass  # Esto se puede modificar es un posibilidad de que algunos enemigos no suelten gema al matarlos
        elif 20 < probability <= 75:
            self.add_experience_gem(ExperienceGem(
                monster.pos_x, monster.pos_y, 1))
        elif 75 < probability <= 80:
            self.add_experience_gem(
                SpeedGem(monster.pos_x, monster.pos_y, 1, speed_boost=10, duration=5))
        elif 80 < probability <= 85:
            self.add_experience_gem(
                DamageGem(monster.pos_x, monster.pos_y, 1, damage_boost=5, duration=5))
        elif 85 < probability <= 90:
            self.add_experience_gem(DefenceGem(
                monster.pos_x, monster.pos_y, 1, defence_boost=3, duration=5))
        else:
            self.add_experience_gem(
                HealthGem(monster.pos_x, monster.pos_y, 1, health_boost=25, duration=5))

    def add_experience_gem(self, gem: IExperienceGem):
        self.__experience_gems.append(gem)

    def remove_experience_gem(self, gem: IExperienceGem):
        self.__experience_gems.remove(gem)

    def add_bullet(self, bullet: IBullet):
        self.__bullets.append(bullet)

    def remove_bullet(self, bullet: IBullet):
        self.__bullets.remove(bullet)

    def clear_all_entities(self):
        """Clears all entities from the world."""
        self.__player = None  # type: ignore
        self.__monsters.clear()
        self.__bullets.clear()
        self.__experience_gems.clear()

    def load_game_data(self, game_data: dict) -> None:
        """Loads game data into the world."""
        self.clear_all_entities()

        # Load player
        player_data = game_data['player']
        timer_data = game_data['timer']
        self.__player = Player.load_player_from_json(player_data)

        # Load monsters
        for monster_type, monster_list in game_data.get('monsters', {}).items():
            for monster_data in monster_list:
                monster = Monster.load_monster_from_json(monster_data)
                self.add_monster(monster)

        # Load bullets
        for bullet_type, bullet_list in game_data.get('bullets', {}).items():
            for bullet_data in bullet_list:
                bullet = Bullet.load_bullet_from_json(bullet_data)
                self.add_bullet(bullet)

        # Load experience gems
        for gem_type, gem_list in game_data.get('gems', {}).items():
            for gem_data in gem_list:
                if gem_type == 'DefenceGem':
                    gem = DefenceGem.load_experience_gem_from_json(gem_data)
                elif gem_type == 'SpeedGem':
                    gem = SpeedGem.load_experience_gem_from_json(gem_data)
                elif gem_type == 'DamageGem':
                    gem = DamageGem.load_experience_gem_from_json(gem_data)
                elif gem_type == 'HealthGem':
                    gem = HealthGem.load_experience_gem_from_json(gem_data)
                else:
                    gem = ExperienceGem.load_experience_gem_from_json(gem_data)

                self.add_experience_gem(gem)

        # Set timer
        self.__timer = game_data['timer']

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
    def timer(self) -> int:
        return self.__timer
