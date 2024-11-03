"""This module contains the implementation of the game world."""

from business.entities.interfaces import IBullet, IExperienceGem, IMonster, IPlayer
from business.world.interfaces import IGameWorld, IMonsterSpawner, ITileMap
from business.handlers.cooldown_handler import CooldownHandler
from business.entities.experience_gem import ExperienceGem
from business.entities.monster import Monster
from business.entities.bullet import Bullet

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

        self.add_experience_gem(ExperienceGem(monster.pos_x, monster.pos_y, 1))

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
        self.__player = None
        self.__monsters.clear()
        self.__bullets.clear()
        self.__experience_gems.clear()

    def load_game_data(self, game_data: dict) -> None:
        """Loads game data into the world."""
        self.clear_all_entities()
        
        # Load player
        self.__player.load_player_from_json(game_data['player'])
        
        # Load monsters
        for monster_data in game_data['monsters']:
            # Create a new monster instance from the JSON data
            monster = Monster.load_monster_from_json(monster ,monster_data)
            
            # Add the newly created monster to the __monsters list
            self.add_monster(monster)
        
        # Load bullets
        for bullet_data in game_data['bullets']:
            bullet = self.load_bullet_from_json(bullet_data)
            self.add_bullet(bullet)
        
        # Load experience gems
        for gem_data in game_data['gems']:
            gem = self.load_experience_gem_from_json(gem_data)
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
