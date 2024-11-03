import os
import json
from collections import defaultdict
from persistence.gamedao import IGameDAO
from business.world.game_world import GameWorld

class GameWorldJsonDAO(IGameDAO):
    """JSON DAO that handles the saving and loading of GameWorld data."""

    BASE_GAME_DATA = {}

    def __init__(self, json_path="data/game_world.json") -> None:
        """Initializes the DAO and creates a JSON file if it does not exist."""
        self.__json_path = json_path
        if not os.path.exists(self.__json_path):
            with open(self.__json_path, 'w', encoding="utf-8") as file:
                json.dump(self.BASE_GAME_DATA, file, indent=4)

    def __read_data(self) -> dict:
        """Reads data from the JSON file."""
        with open(self.__json_path, 'r', encoding="utf-8") as file:
            return json.load(file)

    def __save_data(self, data: dict) -> None:
        """Saves data to the JSON file."""
        with open(self.__json_path, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def save_game(self, game_world: GameWorld) -> None:
        """Serializes and saves the current state of GameWorld."""
        data = self.__read_data()

        monsters = defaultdict(list)
        for monster in game_world.monsters:
            monsters[monster.__class__.__name__].append(monster.json_format())

        bullets = defaultdict(list)
        for bullet in game_world.bullets:
            bullets[bullet.__class__.__name__].append(bullet.json_format())

        experience_gems = defaultdict(list)
        for gem in game_world.experience_gems:
            experience_gems[gem.__class__.__name__].append(gem.json_format())

        player = game_world.player.json_format()
        timer = game_world.timer

        # Update the JSON structure
        data['monsters'] = monsters
        data['bullets'] = bullets
        data['gems'] = experience_gems
        data['player'] = player
        data['timer'] = timer

        self.__save_data(data)

    def load_game(self, game_world: GameWorld) -> None:
        """Loads the saved GameWorld state and populates the provided GameWorld instance."""
        data = self.__read_data()

        # Clear existing entities in the game world
        game_world.clear_all_entities()  # You might need to implement this method in GameWorld

        # Load monsters
        for monster_type, monster_data_list in data.get('monsters', {}).items():
            for monster_data in monster_data_list:
                # You will need a method to create a Monster from the JSON data
                monster = self.create_monster_from_json(monster_data)  
                game_world.add_monster(monster)

        # Load bullets
        for bullet_type, bullet_data_list in data.get('bullets', {}).items():
            for bullet_data in bullet_data_list:
                # You will need a method to create a Bullet from the JSON data
                bullet = self.create_bullet_from_json(bullet_data)
                game_world.add_bullet(bullet)

        # Load experience gems
        for gem_type, gem_data_list in data.get('gems', {}).items():
            for gem_data in gem_data_list:
                # You will need a method to create a Gem from the JSON data
                gem = self.create_experience_gem_from_json(gem_data)
                game_world.add_experience_gem(gem)

        # Load player data
        player_data = data.get('player')
        if player_data:
            game_world.player.load_from_json(player_data)  # You might need to implement this method in the Player class

        # Load timer
        game_world.timer = data.get('timer', 0)  # Set the timer if it exists


    def clear_save(self) -> None:
        """Clears the saved game data."""
        self.__save_data({})
