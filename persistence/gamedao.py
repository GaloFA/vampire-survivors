""" Module that contains interface for gameworld DAO """
from abc import abstractmethod, ABC
from business.world.interfaces import IGameWorld

class IGameDAO(ABC):
    """ Interface for gameworld DAO """

    @abstractmethod
    def add_game(self, game_world):
        """Adds a new savestate to the JSON.

        Args:
            game_world (IGameWorld): The instance of the game world to save..
        """

    @abstractmethod
    def remove_game(self):
        """Removes the saved game state from the data source."""

    @abstractmethod
    def load_game(self) -> IGameWorld:
        """Loads the saved game state and returns an instance of the game world.

        Returns:
            IGameWorld: An instance of the game world with the saved data.
        """

    @abstractmethod
    def has_saved_game_data(self) -> bool:
        """Checks if there is saved game data.

        Returns:
            bool: If there is saved game data.
        """

    @abstractmethod
    def clear_save(self) -> None:
        """Clears the saved game data."""
