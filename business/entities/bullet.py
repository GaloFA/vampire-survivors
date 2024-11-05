"""Module for a bullet entity that moves towards a target direction."""

import math
import settings
from business.entities.entity import MovableEntity
from business.entities.interfaces import IBullet
from business.world.interfaces import IGameWorld
from presentation.sprite import BulletSprite


class Bullet(MovableEntity, IBullet):
    """A bullet that moves towards a target direction."""

    def __init__(self, src_x, src_y, dst_x, dst_y, speed):
        super().__init__(src_x, src_y, speed, BulletSprite(src_x, src_y))
        self.__dir_x, self.__dir_y = self.__calculate_direction(dst_x - src_x, dst_y - src_y)
        self.__health: int = 1
        self.__damage_amount: int = 5
        self.__final_damage_amount: int = 0

    def __calculate_direction(self, dx, dy):
        distance = math.hypot(dx, dy)
        if distance != 0:
            return dx / distance, dy / distance
        return 0, 0

    def take_damage(self, amount):
        self.__health = max(0, self.__health - amount)
        self.sprite.take_damage()

    def update(self, world: IGameWorld):
        self.move(self.__dir_x, self.__dir_y)

        self.__final_damage_amount = self.__damage_amount * world.player.damage_amount

    def __str__(self):
        return f"Bullet(pos=({self._pos_x, self._pos_y}), dir=({self.__dir_x, self.__dir_y}))"

    def json_format(self):
        return {
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'dir_x': self.__dir_x,
            'dir_y': self.__dir_y,
            'damage_amount': self.__damage_amount,
            'health': self.__health,
            'speed': self.speed
        }

    @staticmethod
    def load_bullet_from_json(bullet_data) -> IBullet:
        """Creates a bullet from JSON data."""
        src_x = bullet_data['pos_x']
        src_y = bullet_data['pos_y']
        dir_x = bullet_data['dir_x']
        dir_y = bullet_data['dir_y']
        speed = bullet_data['speed']

        return Bullet(src_x, src_y, dir_x, dir_y, speed)

    @property
    def damage_amount(self):
        return self.__final_damage_amount

    @property
    def health(self) -> int:
        return self.__health
