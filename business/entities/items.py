import random
import pygame
import settings
from business.entities.player import Player
from presentation.sprite import PlayerSprite


class Item:
    """Base class representing a generic item with levels and effects."""

    def __init__(self, name, description, effect_type, upgrades, image_path):
        """
        Initializes an item with a name, description, effect type, level upgrades,
        and optionally an image or sprite with configuration.
        """
        self._name = name
        self._description = description
        self._effect_type = effect_type
        self._upgrades = upgrades
        self._level = 1
        self._image_path = image_path

    def level_up(self, player):
        """Increases the item's level if it hasn't reached the maximum level and applies the upgrade."""
        if self._level < len(self._upgrades):
            self._level += 1
            self.apply_effect(player)
            return f"{self._name} has leveled up to level {self._level} and now grants {self.get_effect_value()} effect!"
        else:
            return f"{self._name} is already at the maximum level."

    def get_effect_value(self):
        return self._upgrades[self._level - 1]

    def apply_effect(self, player):
        """Method to be implemented in subclasses to apply the specific effect to the player."""
        pass

    def __str__(self):
        """Returns a string representation of the item."""
        return f"{self._name} - Level {self._level}"

    @property
    def description(self):
        """Returns the description of the item."""
        return self._description

    @property
    def image_path(self):
        """Returns the image path of the item."""
        return self._image_path


class HealthItem(Item):
    """Item that provides health upgrades."""

    def __init__(self):
        super().__init__(
            name="Health Amulet",
            description="Increases the player's health.",
            effect_type="health",
            upgrades=[20, 40, 60, 80, 100],
            image_path="./assets/items/sprite-items/item2.png"
        )

    def apply_effect(self, player: Player):
        player.set_max_health(self.get_effect_value())

    @property
    def description(self):
        """Returns the description of the item."""
        return self._description

    @property
    def image_path(self):
        """Returns the image path of the item."""
        return self._image_path


class SpeedItem(Item):
    """Item that provides speed upgrades."""

    def __init__(self):
        super().__init__(
            name="Speed Boots",
            description="Increases the player's movement speed.",
            effect_type="speed",
            upgrades=[2, 4, 6, 8, 10],
            image_path="./assets/items/sprite-items/item7.png"
        )

    def apply_effect(self, player: Player):
        player.set_speed(self.get_effect_value())

    @property
    def description(self):
        """Returns the description of the item."""
        return self._description

    @property
    def image_path(self):
        """Returns the image path of the item."""
        return self._image_path


class DamageItem(Item):
    """Item that provides damage upgrades."""

    def __init__(self):
        super().__init__(
            name="Warrior's Sword",
            description="Increases the damage dealt by the player.",
            effect_type="damage",
            upgrades=[5, 10, 15, 20, 25],
            image_path="./assets/items/sprite-items/item5.png"
        )

    def apply_effect(self, player: Player):
        player.set_damage(self.get_effect_value())

    @property
    def description(self):
        """Returns the description of the item."""
        return self._description

    @property
    def image_path(self):
        """Returns the image path of the item."""
        return self._image_path


class DefenceItem(Item):
    """Item that provides defence upgrades."""

    def __init__(self):
        super().__init__(
            name="Shield of the Brave",
            description="Increases the player's defence.",
            effect_type="defence",
            upgrades=[3, 6, 9, 12, 15],
            image_path="./assets/items/sprite-items/item8.png"
        )

    def apply_effect(self, player: Player):
        player.set_defence(self.get_effect_value())

    @property
    def description(self):
        """Returns the description of the item."""
        return self._description

    @property
    def image_path(self):
        """Returns the image path of the item."""
        return self._image_path


class ExperienceItem(Item):
    """Item that provides experience gain upgrades."""

    def __init__(self):
        super().__init__(
            name="Book of Wisdom",
            description="Increases experience gained by the player.",
            effect_type="experience",
            upgrades=[2, 3, 4, 5, 10],
            image_path="./assets/items/sprite-items/item9.png"
        )

    def apply_effect(self, player: Player):
        player.set_experience_mult(self.get_effect_value())

    @property
    def description(self):
        """Returns the description of the item."""
        return self._description

    @property
    def image_path(self):
        """Returns the image path of the item."""
        return self._image_path


class AutoHealItem(Item):
    """Item that improves the player's self-healing."""

    def __init__(self):
        super().__init__(
            name="Petals of Light",
            description="Increases the amount of health automatically restored.",
            effect_type="autoheal",
            upgrades=[1, 2, 3, 4, 5],
            image_path="./assets/items/sprite-items/item11.png"
        )

    def apply_effect(self, player: Player):
        player.set_autoheal(self.get_effect_value())

    @property
    def description(self):
        """Returns the description of the item."""
        return self._description

    @property
    def image_path(self):
        """Returns the image path of the item."""
        return self._image_path

class DictionaryClass:
    def __init__(self):
        # Ensure these items are correct instances of your classes
        self.items_dict = {
            "health_item": HealthItem(),
            "speed_item": SpeedItem(),
            "damage_item": DamageItem(),
            "defence_item": DefenceItem(),
            "experience_item": ExperienceItem(),
            "autoheal_item": AutoHealItem(),
        }
        self._selected_items = {}  # Dictionary to store selected items

    def select_random_items(self):
        """Selects 3 unique random items from the items dictionary."""

        unique_keys = random.sample(list(self.items_dict.keys()), 3)

        self._selected_items = {
            key: self.items_dict[key] for key in unique_keys}
        return self._selected_items
