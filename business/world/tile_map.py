"""Module that contains the TileMap class."""

import settings
from business.world.interfaces import ITileMap


class TileMap(ITileMap):
    """Class that represents the tile map of the game world."""

    def __init__(self):
        self.map_data = self.__generate_tile_map()

    def __generate_tile_map(self):
        # Create a 2D array of tile indices
        tile_map = []

        for row in range(settings.WORLD_ROWS):
            current_row = []
            for col in range(settings.WORLD_COLUMNS):
                if row == 0 or row == settings.WORLD_ROWS - 1 or col == 0 or col == settings.WORLD_COLUMNS - 1:
                    current_row.append(0)
                else:
                    current_row.append(1)
            tile_map.append(current_row)

        return tile_map

    def get(self, row, col) -> int:
        # Get the tile index at a specific row and column
        return self.map_data[row][col]
