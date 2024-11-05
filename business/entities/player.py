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
from business.handlers.cooldown_handler import CooldownHandler
# from game import Game


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

        self.__health: int = health
        self.__max_health: int = 100

        self.__last_shot_time = pygame.time.get_ticks()  # Tiempo del último disparo
        self._last_autoheal_time = pygame.time.get_ticks()

        self.__experience = 0
        self.__multexperience = 1
        self.__level = 1

        self.__speed_base: int = 500
        self.__speed_increase: int = 1
        self.__speed: int = 0

        self.__damage_base: int = 1
        self.__damage_increase: int = 0
        self.__damage: int = 1

        self.__defence_base: int = 0
        self.__defence_increase: int = 0
        self.__defence: int = 0

        self.__autoheal: int = 0

        self.__critical: int = 0

        self.__attack_speed_increase: int = 0

        self.__weapon_type = "pistol"
        self.__weapon = PistolWeapon()

        self.__damage_boost_cooldown = CooldownHandler(5000)
        self.__speed_boost_cooldown = CooldownHandler(5000)
        self.__defence_boost_cooldown = CooldownHandler(5000)
        self.__critical_boost_cooldown = CooldownHandler(5000)

    def json_format(self):
        return {
            'health': self.__health,
            'max_health': self.__max_health,
            'last_shot_time': self.__last_shot_time,
            'experience': self.__experience,
            'multexperience': self.__multexperience,
            'level': self.__level,
            'velocidad': self.__speed,
            'damage': self.__damage,
            'defensa': self.__defence,
            'autoheal': self.__autoheal,
            'critical': self.__critical,
            'velocidad_ataque': self.__attack_speed_increase,
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
        player.__max_health = player_data.get('max_health', player.__max_health)
        player.__last_shot_time = player_data.get('last_shot_time', player.__last_shot_time)
        player.__experience = player_data.get('experience', player.__experience)
        player.__multexperience = player_data.get('multexperience', player.__multexperience)
        player.__level = player_data.get('level', player.__level)
        player.__speed = player_data.get('speed', player.__speed)
        player.__damage = player_data.get('damage', player.__damage)
        player.__defence = player_data.get('defence', player.__defence)
        player.__autoheal = player_data.get('autoheal', player.__autoheal)
        player.__critical = player_data.get('critical', player.__critical)
        player.__attack_speed_increase = player_data.get('velocidad_ataque', player.__attack_speed_increase)
        player.__weapon_type = player_data.get('weapon_type', player.__weapon_type)

        if player.__weapon_type == "pistol":
            player.__weapon = PistolWeapon()
        elif player.__weapon_type == "shotgun":
            player.__weapon = ShotgunWeapon()
        elif player.__weapon_type == "minigun":
            player.__weapon = MinigunWeapon()

        return player

    def aplicar_efecto(self, item):
        if item.tipo_efecto == "salud":
            self.__max_health += item_autoheal.amount
        if item.tipo_efecto == "velocidad":
            self.__speed_increase += item_autoheal.amount
        if item.tipo_efecto == "damage":
            self.__damage_increase += item_autoheal.amount
        if item.tipo_efecto == "defensa":
            self.__defence_increase += item_autoheal.amount
        if item.tipo_efecto == "experiencia":
            self.__experience += item_autoheal.amount
        if item.tipo_efecto == "autoheal":
            self.__health += item_autoheal.amount
        if item.tipo_efecto == "critico":
            self.__critical += item_autoheal.amount
        if item.tipo_efecto == "velocidad_ataque":
            self.__attack_speed_increase += item_autoheal.amount

    def set_timer(self, timer):
        self.__timer = timer

    def __str__(self):
        hp = self.__health
        xp = self.__experience
        lvl = self.__level
        pos = str(self._pos_x) + str(self._pos_y)
        vel = self.__speed_base
        dam = self.__damage_base
        defe = self.__defence_base
        autoc = self.__autoheal
        pcrit = self.__critical
        return (f"Player(hp={hp}, xp={xp}, lvl={lvl}, pos=({pos}), "
                f"vel={vel}, damage={dam}, defensa={defe}, "
                f"autocuración={autoc}, critico={pcrit}, ")

    def mostrar_estadisticas(self):
        """Devuelve un diccionario con las estadísticas del jugador."""
        return {
            'Salud': self.__health,
            'Salud Máxima': self.__max_health,
            'Experiencia': self.__experience,
            'Nivel': self.level,
            'Velocidad': self.speed,
            'Daño': self.damage_amount,
            'Defensa': self.defense_amount,
            'Autocuración': self.__autoheal,
            'Probabilidad Crítico': self.__critical,
            'Velocidad de Ataque': self.__attack_speed_increase,
        }

    @staticmethod
    def set_shoot_cooldown(shoot_cooldown: int):
        Player.BASE_SHOOT_COOLDOWN = shoot_cooldown

    def move(self, dx: int, dy: int):
        """Mueve al jugador, ajustando la distancia según la velocidad actual."""
        super().move(dx * 4000, dy * 4000)

    def take_damage(self, amount):
        if self.__defence_base >= amount:
            amount = 0
        else:
            # Resta el valor de la defensa al daño si es menor que el daño recibido
            amount -= self.__defence_base

        # Actualiza la salud asegurando que no sea menor que 0
        self.__health = max(0, self.__health - amount)
        self.sprite.take_damage()

    def pickup_gem(self, gem: IExperienceGem):
        if isinstance(gem, ExperienceGem):
            amount = gem.amount * self.__multexperience
            self.__gain_experience(amount)
        if isinstance(gem, SpeedGem) and self.__speed_boost_cooldown.is_action_ready():
            self.__speed_increase += 10
            self.increase_speed()
            self.__speed_boost_cooldown.put_on_cooldown()
        if isinstance(gem, DamageGem) and self.__damage_boost_cooldown.is_action_ready():
            self.__damage_increase += 5
            self.__damage_boost_cooldown.put_on_cooldown()
        if isinstance(gem, DefenseGem) and self.__defence_boost_cooldown.is_action_ready():
            self.__defence_increase += 10
            self.__defence_boost_cooldown.put_on_cooldown()
        if isinstance(gem, HealthGem):
            self.__health += 25

    def __levelup_perks(self):
        self.__health *= self.__level
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
        self.__health = min(self.__max_health, self.__health + amount)

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

    def update_stats(self):
        """Update all stats."""
        self.__health = min(self.__max_health, self.__health)

        self.__damage = self.__damage_base + self.__damage_increase
        self.__speed_base += self.__speed_increase
        self.__defence_base += self.__defence_increase

        if self.__critical_boost_cooldown.is_action_ready():
            self.__critical = max(0, self.__critical)

        if self.__speed_boost_cooldown.is_action_ready() and self.__speed_increase > 0:
            self.__speed_increase -= 10
            
        if self.__damage_boost_cooldown.is_action_ready() and self.__damage_increase > 0:
            self.__damage_increase -= 5
        
        if self.__defence_boost_cooldown.is_action_ready() and self.__defence_increase > 0:
            self.__defence_increase -= 10

    def update(self, world: IGameWorld):
        super().update(world)

        current_time = pygame.time.get_ticks()

        self.update_stats()

        if current_time - self._last_autoheal_time >= Player.AUTOHEAL_INTERVAL:
            self.__heal(self.__autoheal)  # Curar al jugador
            # Actualizar el tiempo del último autoheal
            self._last_autoheal_time = current_time

        # if current_time - self.__last_shot_time >= self.__shoot_cooldown:
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
        return self.__damage

    @property
    def health(self) -> int:
        return self.__health

    @property
    def max_health(self):
        return self.__max_health

    @property
    def defense_amount(self):
        return self.__defence

    @property
    def speed(self):
        return self.__speed

    @property
    def __shoot_cooldown(self):
        return Player.BASE_SHOOT_COOLDOWN
