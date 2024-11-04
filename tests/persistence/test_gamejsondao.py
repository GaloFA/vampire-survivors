import unittest
from unittest.mock import MagicMock, patch, mock_open
import json
import os
from persistence.gamejsondao import GameWorldJsonDAO 

class TestGameWorldJsonDAO(unittest.TestCase):

    def setUp(self):
        self.dao = GameWorldJsonDAO(json_path='test_game_world.json')
    
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({}))
    def test_initialization_creates_file(self, mock_file):
        # Check if the JSON file is created during initialization
        if not os.path.exists('test_game_world.json'):
            self.dao.__init__('test_game_world.json')
        self.assertTrue(os.path.exists('test_game_world.json'))
        mock_file.assert_called_once_with('test_game_world.json', 'w', encoding='utf-8')
    
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({}))
    def test_read_data(self, mock_file):
        data = self.dao._GameWorldJsonDAO__read_data()
        self.assertEqual(data, {})  # Expecting an empty dict from the mock
    
    @patch('builtins.open', new_callable=mock_open)
    def test_save_data(self, mock_file):
        self.dao._GameWorldJsonDAO__save_data({'test_key': 'test_value'})
        mock_file.assert_called_once_with('test_game_world.json', 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with(json.dumps({'test_key': 'test_value'}, indent=4))
    
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({}))
    def test_has_saved_game_data_no_data(self, mock_file):
        result = self.dao.has_saved_game_data()
        self.assertFalse(result)
    
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'key': 'value'}))
    def test_has_saved_game_data_with_data(self, mock_file):
        result = self.dao.has_saved_game_data()
        self.assertTrue(result)
    
    @patch('builtins.open', new_callable=mock_open)
    def test_clear_save(self, mock_file):
        self.dao.clear_save()
        mock_file.assert_called_once_with('test_game_world.json', 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with(json.dumps({}, indent=4))
    
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'monsters': {}}))
    @patch.object(GameWorldJsonDAO, '__save_data')
    def test_save_game(self, mock_save_data, mock_file):
        game_world_mock = MagicMock()
        game_world_mock.monsters = []
        game_world_mock.bullets = []
        game_world_mock.experience_gems = []
        game_world_mock.player.json_format.return_value = {'name': 'TestPlayer'}
        game_world_mock.timer = 120

        self.dao.save_game(game_world_mock)
        mock_save_data.assert_called_once()

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'monsters': {}}))
    def test_load_game(self, mock_file):
        game_world_mock = MagicMock()
        game_world_mock.clear_all_entities = MagicMock()
        game_world_mock.load_game_data = MagicMock()

        self.dao.load_game(game_world_mock)
        game_world_mock.clear_all_entities.assert_called_once()
        game_world_mock.load_game_data.assert_called_once_with({'monsters': {}})

    def tearDown(self):
        try:
            os.remove('test_game_world.json')
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    unittest.main()
