"""Module for the CollisionHandler class."""

from typing import List

from business.entities.interfaces import IBullet, IExperienceGem, IHasSprite, IMonster, IPlayer
from business.world.interfaces import IGameWorld


class CollisionHandler:
    """Handles collisions between entities in the game world."""

    @staticmethod
    def __collides_with(an_entity: IHasSprite, another_entity: IHasSprite):
        return an_entity.sprite.rect.colliderect(another_entity.sprite.rect)

    @staticmethod
    def __handle_bullets(bullets: List[IBullet], monsters: List[IMonster]):
        for bullet in bullets:
            for monster in monsters:
                if CollisionHandler.__collides_with(bullet, monster):
                    monster.take_damage(bullet.damage_amount)
                    bullet.take_damage(bullet.damage_amount)

    @staticmethod
    def __handle_monsters(monsters: List[IMonster], player: IPlayer):
        for monster in monsters:
            if CollisionHandler.__collides_with(monster, player):
                player.take_damage(monster.damage_amount)

    @staticmethod
    def __handle_gems(gems: List[IExperienceGem], player: IPlayer, world: IGameWorld):
        for gem in gems:
            if CollisionHandler.__collides_with(gem, player):
                player.pickup_gem(gem)
                world.remove_experience_gem(gem)

    @staticmethod
    def handle_collisions(world: IGameWorld):
        """Handles collisions between entities in the game world.

        Args:
            world (IGameWorld): The game world.
        """
        CollisionHandler.__handle_bullets(world.bullets, world.monsters)
        CollisionHandler.__handle_monsters(world.monsters, world.player)
        CollisionHandler.__handle_gems(world.experience_gems, world.player, world)

    @staticmethod
    def detect_monster_collisions(aMonster: IMonster, monsters: List[IMonster]):
        """Detect collisions between monsters and return a list of colliding pairs.

        Args:
            monsters (List[IMonster]): The list of monsters to check for collisions.

        Returns:
            List[Tuple[IMonster, IMonster]]: A list of tuples containing colliding monsters.
        """
        colliding_pairs = []
        for i in range(len(monsters)):
            if monsters[i] == aMonster:
                monster_a = aMonster
                monster_b = monsters[i]
                if CollisionHandler.__collides_with(monster_a, monster_b):
                    colliding_pairs.append((monster_b))
                    colliding_monsters = {monster for monster in colliding_pairs}
        return colliding_monsters