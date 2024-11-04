import os
import json
import unittest
from unittest.mock import MagicMock, patch, mock_open
from collections import defaultdict
from persistence.gamedao import IGameDAO
from business.world.game_world import GameWorld
from business.world.interfaces import IGameWorld
from persistence.gamejsondao import GameWorldJsonDAO


class TestGameWorldJsonDAO(unittest.TestCase):
    def setUp(self):
        self.json_path = "test_game_world.json"  # Use a test path
        self.dao = GameWorldJsonDAO(self.json_path)

    def tearDown(self):
        # Clean up the test JSON file after each test
        if os.path.exists(self.json_path):
            os.remove(self.json_path)

    @patch("builtins.open", new_callable=mock_open, read_data='{}')
    @patch("os.path.exists", return_value=False)
    def test_initialization_creates_file(self, mock_exists, mock_open):
        """Test if the JSON file is created on initialization."""
        self.dao = GameWorldJsonDAO(self.json_path)
        mock_open.assert_called_once_with(
            self.json_path, 'w', encoding="utf-8")
        mock_open().write.assert_called_once_with(
            json.dumps(self.dao.BASE_GAME_DATA, indent=4))

    @patch('builtins.open')
    @patch.object(GameWorldJsonDAO, '_GameWorldJsonDAO__read_data')
    @patch.object(GameWorldJsonDAO, '_GameWorldJsonDAO__save_data')
    def test_save_game(self, mock_save_data, mock_read_data, mock_open):
        """Test the save_game method."""
        
        mock_game_world = MagicMock(spec=IGameWorld)

        mock_monster = MagicMock()
        mock_monster.json_format.return_value = {'type': 'Goblin'}
        
        mock_bullet = MagicMock()
        mock_bullet.json_format.return_value = {'type': 'Bullet'}
        
        mock_gem = MagicMock()
        mock_gem.json_format.return_value = {'type': 'Gem'}
        
        mock_game_world.monsters = [mock_monster]
        mock_game_world.bullets = [mock_bullet]
        mock_game_world.experience_gems = [mock_gem]
        mock_game_world.player = MagicMock(json_format=MagicMock(return_value={'name': 'Player1'}))
        mock_game_world.timer = 123
        mock_read_data.return_value = {}

        self.dao.save_game(mock_game_world)

        mock_read_data.assert_called_once()

        expected_data = {
            'monsters': defaultdict(list, {'MagicMock': [{'type': 'Goblin'}]}),
            'bullets': defaultdict(list, {'MagicMock': [{'type': 'Bullet'}]}),
            'gems': defaultdict(list, {'MagicMock': [{'type': 'Gem'}]}),
            'player': {'name': 'Player1'},
            'timer': 123
        }
        mock_save_data.assert_called_once_with(expected_data)

    @patch("builtins.open", new_callable=mock_open, read_data='{"player": {"player_name": "Hero"}}')
    @patch("os.path.getsize", return_value=100)
    @patch("os.path.isfile", return_value=True)
    def test_has_saved_game_data(self, mock_isfile, mock_getsize, mock_open):
        """Test if saved game data is recognized."""
        result = self.dao.has_saved_game_data()
        self.assertTrue(result)

    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    @patch("os.path.getsize", return_value=100)
    @patch("os.path.isfile", return_value=True)
    def test_has_saved_game_data_invalid_json(self, mock_isfile, mock_getsize, mock_open):
        """Test if invalid JSON returns False for saved game data."""
        result = self.dao.has_saved_game_data()
        self.assertFalse(result)

    @patch("builtins.open", new_callable=mock_open)
    def test_clear_save(self, mock_open):
        """Test clearing the saved game data."""
        self.dao.clear_save()
        mock_open().write.assert_called_once_with(json.dumps({}, indent=4))

    @patch("builtins.open", new_callable=mock_open, read_data='{"monsters": {}, "player": {}}')
    @patch("os.path.exists", return_value=True)
    def test_load_game(self, mock_exists, mock_open):
        """Test loading game data into the game world."""
        game_world = MagicMock(spec=IGameWorld)
        game_world.clear_all_entities = MagicMock()
        game_world.load_game_data = MagicMock()

        self.dao.load_game(game_world)

        game_world.clear_all_entities.assert_called_once()
        game_world.load_game_data.assert_called_once_with(
            json.loads(mock_open().read()))

if __name__ == '__main__':
    unittest.main()
