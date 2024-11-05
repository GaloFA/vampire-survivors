"""Player entity module."""

import pygame
import settings
from business.entities.bullet import Bullet
from business.entities.entity import MovableEntity
from business.entities.experience_gem import *
from business.entities.interfaces import ICanDealDamage, IDamageable, IPlayer
from business.world.interfaces import IGameWorld
from presentation.sprite import Sprite, PlayerSprite
from business.entities.weapons import PistolWeapon, ShotgunWeapon, MinigunWeapon
#from game import Game


class Player(MovableEntity, IPlayer, IDamageable, ICanDealDamage):
    """Player entity.

    The player is the main character of the game. 
    It can move around the game world and shoot at monsters.
    """
    AUTOHEAL_INTERVAL = 1000
    BASE_DAMAGE = 1
    BASE_SHOOT_COOLDOWN = 200

    def __init__(self, pos_x: int, pos_y: int, sprite: Sprite, health: int):
        super().__init__(pos_x, pos_y, 5, sprite)

        self.__health_base: int = health
        self.__max_health: int = 100
        self.__last_shot_time = pygame.time.get_ticks()  # Tiempo del último disparo
        self._last_autoheal_time = pygame.time.get_ticks()
        self.__experience = 0
        self.__multexperience = 1
        self.__level = 1
        self.__velocidad_base: int = 500
        self.__velocidad_incrementada: int = 1
        self.__damage_base: int = 10
        self.__damage_incrementada: int = 20
        self.__defensa_base: int = 0
        self.__defensa_incrementada: int = 10
        self.__autocuracion: int = 0
        self.__probabilidad_critico: int = 0
        self.__velocidad_ataque_incrementada: int = 0
        self.__weapon_type = "pistol"
        self.__weapon = PistolWeapon()
        self.__timer = 0

    def json_format(self):
        return {
            'health': self.__health_base,
            'max_health': self.__max_health,
            'last_shot_time': self.__last_shot_time,
            'experience': self.__experience,
            'multexperience': self.__multexperience,
            'level': self.__level,
            'velocidad': self.__velocidad_base,
            'damage': self.__damage_base,
            'defensa': self.__defensa_base,
            'autocuracion': self.__autocuracion,
            'probabilidad_critico': self.__probabilidad_critico,
            'velocidad_ataque': self.__velocidad_ataque_incrementada,
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'weapon_type': self.__weapon_type,
        }

    @staticmethod
    def load_player_from_json(player_data) -> IPlayer:
        """Loads the player entity from JSON data."""
        src_x = player_data['pos_x']
        src_y = player_data['pos_y']
        health = player_data['health']
        sprite = PlayerSprite(src_x, src_y)
        player = Player(src_x, src_y, sprite, health)

        # Load player attributes
        player.__max_health = player_data.get('max_health', player.__max_health)
        player.__last_shot_time = player_data.get('last_shot_time', player.__last_shot_time)
        player.__experience = player_data.get('experience', player.__experience)
        player.__multexperience = player_data.get('multexperience', player.__multexperience)
        player.__max_health = player_data.get(
            'max_health', player.__max_health)
        player.__last_shot_time = player_data.get(
            'last_shot_time', player.__last_shot_time)
        player.__experience = player_data.get(
            'experience', player.__experience)
        player.__multexperience = player_data.get(
            'multexperience', player.__multexperience)
        player.__level = player_data.get('level', player.__level)
        player.__velocidad_base = player_data.get(
            'velocidad', player.__velocidad_base)
        player.__damage_base = player_data.get('damage', player.__damage_base)
        player.__defensa_base = player_data.get(
            'defensa', player.__defensa_base)
        player.__autocuracion = player_data.get(
            'autocuracion', player.__autocuracion)
        player.__probabilidad_critico = player_data.get(
            'probabilidad_critico', player.__probabilidad_critico)
        player.__velocidad_ataque_incrementada = player_data.get(
            'velocidad_ataque', player.__velocidad_ataque_incrementada)
        player.__weapon_type = player_data.get(
            'weapon_type', player.__weapon_type)

        # Assign the weapon based on weapon type loaded from JSON
        if player.__weapon_type == "pistol":
            player.__weapon = PistolWeapon()
        elif player.__weapon_type == "shotgun":
            player.__weapon = ShotgunWeapon()
        elif player.__weapon_type == "minigun":
            player.__weapon = MinigunWeapon()

        return player

    def aplicar_efecto(self, item):
        if item.tipo_efecto == "salud":
            self.__max_health += item_autocuracion.amount
        if item.tipo_efecto == "velocidad":
            self.__velocidad_incrementada += item_autocuracion.amount
        if item.tipo_efecto == "damage":
            self.__damage_incrementada += item_autocuracion.amount
        if item.tipo_efecto == "defensa":
            self.__defensa_incrementada += item_autocuracion.amount
        if item.tipo_efecto == "experiencia":
            self.__experience += item_autocuracion.amount
        if item.tipo_efecto == "autocuracion":
            self.__health_base += item_autocuracion.amount
        if item.tipo_efecto == "critico":
            self.__probabilidad_critico += item_autocuracion.amount
        if item.tipo_efecto == "velocidad_ataque":
            self.__velocidad_ataque_incrementada += item_autocuracion.amount
            
    
    def set_timer(self, timer):
        self.__timer = timer

    def __str__(self):
        hp = self.__health_base
        xp = self.__experience
        lvl = self.__level
        pos = str(self._pos_x) + str(self._pos_y)
        vel = self.__velocidad_base
        dam = self.__damage_base
        defe = self.__defensa_base
        autoc = self.__autocuracion
        pcrit = self.__probabilidad_critico
        return (f"Player(hp={hp}, xp={xp}, lvl={lvl}, pos=({pos}), "
                f"vel={vel}, damage={dam}, defensa={defe}, "
                f"autocuración={autoc}, critico={pcrit}, ")

    def mostrar_estadisticas(self):
        """Devuelve un diccionario con las estadísticas del jugador."""
        return {
            'Salud': self.__health_base,
            'Salud Máxima': self.__max_health,
            'Experiencia': self.__experience,
            'Nivel': self.level,
            'Velocidad': self.speed,  # Llamamos a la propiedad
            'Daño': self.damage_amount,  # Llamamos a la propiedad
            'Defensa': self.defense_amount,  # Llamamos a la propiedad
            'Autocuración': self.__autocuracion,
            'Probabilidad Crítico': self.__probabilidad_critico,
            'Velocidad de Ataque': self.__velocidad_ataque_incrementada,
        }


    @staticmethod
    def set_shoot_cooldown(shoot_cooldown: int):
        Player.BASE_SHOOT_COOLDOWN = shoot_cooldown

    def increase_speed(self):
        """Aumenta la velocidad del jugador."""
        self.__velocidad_base += self.__velocidad_incrementada

    def move(self, dx: int, dy: int):
        """Mueve al jugador, ajustando la distancia según la velocidad actual."""
        super().move(dx * self.__velocidad_base, dy * self.__velocidad_base)

    def take_damage(self, amount):
        if self.__defensa_base >= amount:
            amount = 0
        else:
            # Resta el valor de la defensa al daño si es menor que el daño recibido
            amount -= self.__defensa_base

        # Actualiza la salud asegurando que no sea menor que 0
        self.__health_base = max(0, self.__health_base - amount)
        self.sprite.take_damage()

    def pickup_gem(self, gem: IExperienceGem):
        if isinstance(gem, ExperienceGem):
            amount = gem.amount * self.__multexperience
            self.__gain_experience(amount)
        if isinstance(gem, SpeedGem):
            self.__velocidad_incrementada += 10
            self.increase_speed()
        if isinstance(gem, DamageGem):
            self.__damage_incrementada += 5
        if isinstance(gem, DefenseGem):
            self.__defensa_incrementada += 10
        if isinstance(gem, HealthGem):
            if self.__health_base + 25 >= self.__max_health:
                self.__health_base = self.__max_health
            else:
                self.__health_base += 25


    def __levelup_perks(self):
        self.__health_base *= self.__level
        self.__max_health *= self.__level

        if self.__level == 1:
            self.__weapon = PistolWeapon()
            self.__weapon_type = "pistol"
        if self.__level == 3:
            self.__weapon = ShotgunWeapon()
            self.__weapon_type = "shotgun"
        if self.__level == 6:
            self.__weapon = MinigunWeapon()
            self.__weapon_type = "minigun"

    def __heal(self, amount: int):
        # Aumenta la salud del jugador, asegurándose de que no exceda el máximo
        self.__health_base = min(
            self.__max_health, self.__health_base + amount)

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

        self.__weapon.shoot(world, self.pos_x, self.pos_y,
                            monster.pos_x, monster.pos_y)

    def update(self, world: IGameWorld):
        super().update(world)

        current_time = pygame.time.get_ticks()

        if current_time - self._last_autoheal_time >= Player.AUTOHEAL_INTERVAL:
            self.__heal(self.__autocuracion)  # Curar al jugador
            # Actualizar el tiempo del último autoheal
            self._last_autoheal_time = current_time

        #if current_time - self.__last_shot_time >= self.__shoot_cooldown:
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
        return self.__damage_base + self.__damage_incrementada

    @property
    def health(self) -> int:
        return self.__health_base

    @property
    def max_health(self):
        return self.__max_health

    @property
    def defense_amount(self):
        return self.__defensa_base + self.__defensa_incrementada

    @property
    def speed(self):
        return self.__velocidad_base + self.__velocidad_incrementada

    @property
    def __shoot_cooldown(self):
        return Player.BASE_SHOOT_COOLDOWN
