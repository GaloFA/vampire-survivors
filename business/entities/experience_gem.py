"""Module for the ExperienceGem class."""

from business.entities.entity import Entity
from business.entities.interfaces import IExperienceGem
from presentation.sprite import ExperienceGemSprite


class ExperienceGem(Entity, IExperienceGem):
    """Represents an experience gem in the game world."""

    def __init__(self, pos_x: float, pos_y: float, amount: int):
        super().__init__(pos_x, pos_y, ExperienceGemSprite(pos_x, pos_y))
        self.__amount = amount

    def json_format(self):
        return {
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'amount': self.__amount,
        }

    def load_experience_gem_from_json(self, gem_data) -> IExperienceGem:
        """Creates an experience gem from JSON data."""
        src_x = gem_data['pos_x']
        src_y = gem_data['pos_y']
        amount = gem_data['amount']

        return ExperienceGem(src_x, src_y, amount)

    @property
    def amount(self) -> int:
        return self.__amount

    def __str__(self):
        return f"ExperienceGem(amount={self.__amount}, pos=({self.pos_x}, {self.pos_y}))"
