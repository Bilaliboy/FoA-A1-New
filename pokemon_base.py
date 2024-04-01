"""
This module contains PokeType, TypeEffectiveness and an abstract version of the Pokemon Class
"""
from abc import ABC
from enum import Enum
from data_structures.referential_array import ArrayR
from math import ceil

class PokeType(Enum):
    """
    This class contains all the different types that a Pokemon could belong to
    """
    FIRE = 0
    WATER = 1
    GRASS = 2
    BUG = 3
    DRAGON = 4
    ELECTRIC = 5
    FIGHTING = 6
    FLYING = 7
    GHOST = 8
    GROUND = 9
    ICE = 10
    NORMAL = 11
    POISON = 12
    PSYCHIC = 13
    ROCK = 14

class TypeEffectiveness:
    """
    Represents the type effectiveness of one Pokemon type against another.
    """
    EFFECT_TABLE = ((0.5,0.5,2.0,0.5,0.5,1.0,1.0,1.0,1.0,2.0,2.0,1.0,1.0,1.0,0.5),#Fire     index 0
                (2.0,0.5,0.5,1.0,0.5,1.0,1.0,1.0,1.0,2.0,1.0,1.0,1.0,1.0,2.0),#Water    index 1
                (0.5,2.0,0.5,2.0,0.5,1.0,1.0,2.0,1.0,0.5,2.0,1.0,2.0,1.0,1.0),#Grass    index 2
                (2.0,1.0,0.5,1.0,1.0,1.0,0.5,2.0,0.5,1.0,1.0,1.0,1.0,2.0,1.0),#Bug      index 3
                (1.0,1.0,1.0,1.0,2.0,0.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0),#dragon   index 4
                (1.0,2.0,0.5,1.0,0.5,0.5,1.0,2.0,1.0,0.0,1.0,1.0,1.0,1.0,1.0),#electric index 5
                (1.0,1.0,1.0,0.5,1.0,1.0,1.0,0.5,0.0,1.0,2.0,2.0,0.5,2.0,0.5),#fighting index 6
                (1.0,1.0,0.5,2.0,1.0,2.0,2.0,1.0,1.0,0.5,1.0,1.0,1.0,1.0,2.0),#flying   index 7
                (1.0,1.0,1.0,1.0,1.0,1.0,0.0,1.0,2.0,1.0,1.0,0.5,1.0,0.5,1.0),#ghost    index 8
                (0.5,2.0,0.5,1.0,1.0,2.0,1.0,0.0,1.0,2.0,1.0,1.0,0.5,1.0,2.0),#ground   index 9
                (2.0,1.0,1.0,1.0,1.0,1.0,2.0,2.0,1.0,1.0,0.5,1.0,1.0,1.0,2.0),#ice      index 10
                (1.0,1.0,1.0,1.0,1.0,1.0,2.0,1.0,0.0,1.0,1.0,1.0,1.0,1.0,1.0),#normal   index 11
                (1.0,1.0,2.0,2.0,1.0,1.0,0.5,1.0,0.5,2.0,1.0,1.0,0.5,2.0,1.0),#poison   index 12
                (1.0,1.0,1.0,1.0,1.0,1.0,2.0,1.0,1.0,1.0,1.0,2.0,2.0,0.5,1.0),#psychic  index 13
                (0.5,2.0,1.0,1.0,1.0,1.0,0.5,0.5,1.0,2.0,2.0,1.0,1.0,1.0,2.0))#rock     index 14

    @classmethod
    def get_effectiveness(cls, attack_type: PokeType, defend_type: PokeType) -> float:
        """
        Returns the effectiveness of one Pokemon type against another, as a float.

        Parameters:
            attack_type (PokeType): The type of the attacking Pokemon.
            defend_type (PokeType): The type of the defending Pokemon.

        Returns:
            float: The effectiveness of the attack, as a float value between 0 and 4.
        """
        #Planning for how to get the effectiveness of a Pokemon
        
        return cls.EFFECT_TABLE[attack_type.value][defend_type.value]

    def __len__(self) -> int:
        """
        Returns the number of types of Pokemon
        """
        return len(self.EFFECT_TABLE)

class Pokemon(ABC): # pylint: disable=too-few-public-methods, too-many-instance-attributes
    """
    Represents a base Pokemon class with properties and methods common to all Pokemon.
    """
    def __init__(self):
        """
        Initializes a new instance of the Pokemon class.
        """
        self.health = None
        self.level = None
        self.poketype = None
        self.battle_power = None
        self.evolution_line = None
        self.name = None
        self.experience = None
        self.defence = None
        self.speed = None

    def get_name(self) -> str:
        """
        Returns the name of the Pokemon.

        Returns:
            str: The name of the Pokemon.
        """
        return self.name

    def get_health(self) -> int:
        """
        Returns the current health of the Pokemon.

        Returns:
            int: The current health of the Pokemon.
        """
        return self.health

    def get_level(self) -> int:
        """
        Returns the current level of the Pokemon.

        Returns:
            int: The current level of the Pokemon.
        """
        return self.level

    def get_speed(self) -> int:
        """
        Returns the current speed of the Pokemon.

        Returns:
            int: The current speed of the Pokemon.
        """
        return self.speed

    def get_experience(self) -> int:
        """
        Returns the current experience of the Pokemon.

        Returns:
            int: The current experience of the Pokemon.
        """
        return self.experience

    def get_poketype(self) -> PokeType:
        """
        Returns the type of the Pokemon.

        Returns:
            PokeType: The type of the Pokemon.
        """
        return self.poketype

    def get_defence(self) -> int:
        """
        Returns the defence of the Pokemon.

        Returns:
            int: The defence of the Pokemon.
        """
        return self.defence

    def get_evolution(self):
        """
        Returns the evolution line of the Pokemon.

        Returns:
            list: The evolution of the Pokemon.
        """
        return self.evolution_line

    def get_battle_power(self) -> int:
        """
        Returns the battle power of the Pokemon.

        Returns:
            int: The battle power of the Pokemon.
        """
        return self.battle_power

    def attack(self, other_pokemon) -> int:
        """
        Calculates and returns the damage that this Pokemon inflicts on the
        other Pokemon during an attack.

        Args:
            other_pokemon (Pokemon): The Pokemon that this Pokemon is attacking.

        Returns:
            int: The damage that this Pokemon inflicts on the other Pokemon during an attack.
        """
        defence = other_pokemon.get_defence()
        attack = self.get_battle_power()
        attack_type = self.get_poketype()
        defend_type = other_pokemon.get_poketype()

        if defence < attack / 2:
            damage = attack - defence
        elif defence < attack:
            damage = ceil((attack * 5/8) - (defence / 4))
        else:
            damage = ceil(attack / 4)
        
        yoMama = TypeEffectiveness()
        effectiveness = yoMama.get_effectiveness(attack_type, defend_type)
        damage_dealt = int(effectiveness) * damage
        return damage_dealt

    def defend(self, damage: int) -> None:
        """
        Reduces the health of the Pokemon by the given amount of damage, after taking
        the Pokemon's defence into account.

        Args:
            damage (int): The amount of damage to be inflicted on the Pokemon.
        """
        effective_damage = damage/2 if damage < self.get_defence() else damage
        self.health = self.health - effective_damage

    def level_up(self) -> None:
        """
        Increases the level of the Pokemon by 1, and evolves the Pokemon if it has
          reached the level required for evolution.
        """
        self.level += 1
        if len(self.evolution_line) > 0 and self.evolution_line.index\
            (self.name) != len(self.evolution_line)-1:
            self._evolve()

    def _evolve(self) -> None:
        """
        Evolves the Pokemon to the next stage in its evolution line, and updates
          its attributes accordingly.
        """
        next_index = self.evolution_line.index(self.name) + 1
        if next_index < len(self.evolution_line):
            self.name = self.evolution_line[next_index]    
            self.health = int(self.health * 1.5)
            self.speed = int(self.speed * 1.5)
            self.defence = int(self.defence * 1.5)
            self.battle_power = int(self.battle_power * 1.5)
        else:
            print(f"the Pokemon {self.name} cannot be evolved to the next stage")
        return None

    def is_alive(self) -> bool:
        """
        Checks if the Pokemon is still alive (i.e. has positive health).

        Returns:
            bool: True if the Pokemon is still alive, False otherwise.
        """
        return self.get_health() > 0

    def __str__(self):
        """
        Return a string representation of the Pokemon instance in the format:
        <name> (Level <level>) with <health> health and <experience> experience
        """
        return f"{self.name} (Level {self.level}) with {self.get_health()} health and {self.get_experience()} experience"
    def get__attribute__by__criteria(self, criteria):
        """
        Returns the value of the attribute specified by the criteria string.

        Parameters:
        criteria (str): The criteria string specifying the attribute.

        Returns:
        The value of the requested attribute, or None if the criteria is invalid.
        """
        if criteria == "health":
            return self.get_health()
        elif criteria == "level":
            return self.get_level()
        elif criteria == "speed":
            return self.get_speed()
        elif criteria == "experience":
            return self.get_experience()
        elif criteria == "poketype":
            return self.get_poketype()
        elif criteria == "defence":
            return self.get_defence()
        elif criteria == "battle_power":
            return self.get_battle_power()