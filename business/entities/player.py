"""Player entity module."""

import pygame
import settings
from business.entities.bullet import Bullet
from business.entities.entity import MovableEntity
from business.entities.experience_gem import ExperienceGem
from business.entities.interfaces import ICanDealDamage, IDamageable, IPlayer
from business.world.interfaces import IGameWorld
from presentation.sprite import Sprite


class Player(MovableEntity, IPlayer, IDamageable, ICanDealDamage):
    """Player entity.

    The player is the main character of the game. 
    It can move around the game world and shoot at monsters.
    """

    BASE_DAMAGE = 10
    BASE_SHOOT_COOLDOWN = 200

    def __init__(self, pos_x: int, pos_y: int, sprite: Sprite, health: int):
        super().__init__(pos_x, pos_y, 5, sprite)

        self.__health: int = health                 # Salud actual
        self.__max_health: int = 100             # Salud máxima
        self.__last_shot_time = pygame.time.get_ticks()  # Tiempo del último disparo
        self.__experience = 0                     # Experiencia acumulada
        self.__level = 1                          # Nivel del jugador
        self.__velocidad: int = 5                 # Velocidad de movimiento del jugador
        self.__damage: int = 10                    # Daño infligido por el jugador
        self.__defensa: int = 0                   # Defensa del jugador
        self.__autocuracion: int = 0              # Mejora de autocuración del jugador
        # Probabilidad de infligir damage crítico
        self.__probabilidad_critico: int = 0
        self.__velocidad_ataque: int = 1

    def json_format(self):
        return {
            'health': self.__health,
            'max_health': self.__max_health,
            'last_shot_time': self.__last_shot_time,
            'experience': self.__experience,
            'level': self.__level,
            'velocidad': self.__velocidad,
            'damage': self.__damage,
            'defensa': self.__defensa,
            'autocuracion': self.__autocuracion,
            'probabilidad_critico': self.__probabilidad_critico,
            'velocidad_ataque': self.__velocidad_ataque,
        }

    def load_player_from_json(self, player_data) -> IPlayer:
        """Loads the player entity from JSON data."""
        src_x = player_data['pos_x']
        src_y = player_data['pos_y']
        health = player_data['health']
        sprite = player_data['sprite']

        return Player(src_x, src_y, sprite, health)

    def __str__(self):
        hp = self.__health
        xp = self.__experience
        lvl = self.__level
        pos = str(self._pos_x) + str(self._pos_y)
        vel = self.__velocidad
        dam = self.__damage
        defe = self.__defensa
        autoc = self.__autocuracion
        pcrit = self.__probabilidad_critico
        velata = self.__velocidad_ataque
        return (f"Player(hp={hp}, xp={xp}, lvl={lvl}, pos=({pos}), "
                f"vel={vel}, damage={dam}, defensa={defe}, "
                f"autocuración={autoc}, critico={pcrit}, "
                f"vel_ataque={velata})")

    def mostrar_estadisticas(self):
        pass

    def take_damage(self, amount):
        self.__health = max(0, self.__health - amount)  # - amount
        self.sprite.take_damage()

    def pickup_gem(self, gem: ExperienceGem):
        self.__gain_experience(gem.amount)

    def __levelup_perks(self):
        self.__health *= self.__level
        self.__max_health *= self.__level

    def __gain_experience(self, amount: int):
        self.__experience += amount
        while self.__experience >= self.experience_to_next_level:
            self.__experience -= self.experience_to_next_level
            self.__level += 1
            self.__levelup_perks()

    def __shoot_at_nearest_enemy(self, world: IGameWorld):
        if not world.monsters:
            return

        monster = min(
            world.monsters,
            key=lambda monster: (
                (monster.pos_x - self.pos_x) ** 2 +
                (monster.pos_y - self.pos_y) ** 2
            ),
        )

        bullet = Bullet(self.pos_x, self.pos_y,
                        monster.pos_x, monster.pos_y, 10)
        world.add_bullet(bullet)

    def update(self, world: IGameWorld):
        super().update(world)

        current_time = pygame.time.get_ticks()
        if current_time - self.__last_shot_time >= self.__shoot_cooldown:
            self.__shoot_at_nearest_enemy(world)
            self.__last_shot_time = current_time

    @property
    def experience(self):
        return self.__experience

    @property
    def experience_to_next_level(self):
        base_xp = 2
        if self.__level == 1:
            return base_xp
        return base_xp * (2 ** (self.__level - 1))

    @property
    def level(self):
        return self.__level

    @property
    def damage_amount(self):
        return Player.BASE_DAMAGE

    @property
    def health(self) -> int:
        return self.__health

    @property
    def max_health(self):
        return self.__max_health

    @property
    def __shoot_cooldown(self):
        return Player.BASE_SHOOT_COOLDOWN
