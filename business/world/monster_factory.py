"""This module contains the MonsterFactory class, which creates Monster instances."""

from business.entities.monster import Monster
from presentation.sprite import Sprite

class MonsterFactory:
    """Factory for creating Monster instances with custom configurations."""

    def __init__(self, default_health=10, default_damage=5, default_attack_range=50, default_max_health = 10):
        self.default_health = default_health
        self.default_damage = default_damage
        self.default_attack_range = default_attack_range
        self.default_max_health = default_max_health

    def create_zombie(self, src_x: int, src_y: int, sprite: Sprite) -> Monster:
        """Creates zombie monster."""
        monster = Monster(src_x, src_y, sprite, self.default_health, self.default_max_health, self.default_damage, self.default_attack_range)

        return monster
    
    def create_skeleton(self, src_x: int, src_y: int, sprite: Sprite) -> Monster:
        """Creates orc monster."""
        monster = Monster(src_x, src_y, sprite, 15, 15, 10, 50)

        return monster

    def create_orc(self, src_x: int, src_y: int, sprite: Sprite) -> Monster:
        """Creates orc monster."""
        monster = Monster(src_x, src_y, sprite, 20, 20, 15, 60)

        return monster
    
    def create_werewolf(self, src_x: int, src_y: int, sprite: Sprite) -> Monster:
        """Creates werewolf monster."""
        monster = Monster(src_x, src_y, sprite, 25, 25, 20, 60)

        return monster
