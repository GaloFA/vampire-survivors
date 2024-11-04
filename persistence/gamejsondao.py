import os
import json
from collections import defaultdict
from persistence.gamedao import IGameDAO
from business.world.game_world import GameWorld
from business.world.interfaces import IGameWorld

class GameWorldJsonDAO(IGameDAO):
    """JSON DAO that handles the saving and loading of GameWorld data."""

    BASE_GAME_DATA = {}

    def __init__(self, json_path="persistence/data/game_world.json") -> None:
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

    def save_game(self, game_world: IGameWorld) -> None:
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

    def load_game(self, game_world: IGameWorld) -> None:
        """Loads the saved GameWorld state and populates the provided GameWorld instance."""
        data = self.__read_data()

        game_world.clear_all_entities()

        game_world.load_game_data(data)

    def has_saved_game_data(self) -> bool:
        """Checks if there is saved game data available to load."""
        if os.path.isfile(self.__json_path) and os.path.getsize(self.__json_path) > 10:
            try:
                with open(self.__json_path, 'r') as file:
                    data = json.load(file)
                return bool(data)
            except json.JSONDecodeError:
                return False
        return False

    def clear_save(self) -> None:
        """Clears the saved game data."""
        self.__save_data({})
