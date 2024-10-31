# factory.py
"""This module contains the MonsterFactory class, which creates Monster instances."""

from business.entities.monster import Monster
from presentation.sprite import Sprite

class MonsterFactory:
    """Factory for creating Monster instances with custom configurations."""

    def __init__(self, default_health=10, default_damage=10, default_attack_range=50):
        self.default_health = default_health
        self.default_damage = default_damage
        self.default_attack_range = default_attack_range

    def create_monster(self, src_x: int, src_y: int, sprite: Sprite) -> Monster:
        """Creates a Monster with predefined or default attributes."""
        monster = Monster(src_x, src_y, sprite)
        
        monster.__health = self.default_health
        monster.__damage = self.default_damage
        monster.__attack_range = self.default_attack_range
        
        return monster

    def create_orc(self, src_x: int, src_y: int, sprite: Sprite) -> Monster:
        """Creates an Orc monster."""
        orc = Monster(src_x, src_y, sprite)

        orc.__health = 20
        orc.__damage = 15
        orc.__attack_range = 60

        return orc