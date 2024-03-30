from pokemon import *
import random
from typing import List
from battle_mode import BattleMode
from data_structures.referential_array import ArrayR
from data_structures.set_adt import Set

'''	
class ArraySet(Set[T]):
    #Time complexity O(n * Comp==) best case is O(Comp==)
    MIN_CAPACITY = 1
    def __init__(self, capacity: int = 1) -> None:
        set.__innit_self__(self)
        self.array = ArrayR(max(self.MIN_CAPACITY, capacity))
    #O(1)
    def clear(self) -> None:
        self.size = 0

    #O(1)
    def __len__(self) -> int:
        return self.size
    #O(1)
    def is_empty(self) -> bool:
        return len(self) == 0
    #O(1)
    def is_full(self) -> bool:
        return len(self) == len(self.array)
    
    #time complexity is O(N * Comp==) where N is the size of set. best case is O(1).
    def __contains__(self, item: T) -> bool:
        for i in range(self.size):
            if item == self.array[i]:
                return True
        return False
    
    #time complexity is O(N * Comp==) best case O(1).
    def remove(self, item: T) -> None:
        for i in range(self.size):
            if item == self.array[i]:
                self.array[i] = self.array[self.size - 1]
                self.size -= 1
            break
        else:
            raise KeyError(item)
    
    #time complexity is O(N * Comp==) and best case is O(1).
    def add(self, item: T) -> None:
        if item not in self:
            if self.is_full():
                raise Exception("Set is full")
        self.array[self.size] = item
        self.size += 1
    
    #N and M are the size of self and other. Time complexity is O(M *(M+N).
    def union(self, other: ArraySet[T]) -> ArraySet[T]:  # let n = |self|, m = |other|
        res = ArraySet(len(self.array) + len(other.array))  # O(n + m)
        for i in range(len(self)):       # n times
            res.array[i] = self.array[i] # O(1)
        res.size = self.size             # O(1)
        for j in range(len(other)):           # m times
            if other.array[j] not in self:    # O(n * comp)
                res.array[res.size] = other.array[j] # O(1)
                res.size += 1                        # O(1)
        return res
    
'''	    






class PokeTeam:
    TEAM_LIMIT = 6
    POKE_LIST = get_all_pokemon_types()
    CRITERION_LIST = ["health", "defence", "battle_power", "speed", "level"]

    def __init__(self):
        self.team = ArrayR(self.TEAM_LIMIT) # change None value if necessary
        self.team_count = 0

#How to find pokemon in pokeType.
    #Timecomplexity is O(Comp==) best case and O(n * Comp==) for worst case. Where n is the pokemon classes.
    def find_pokemon_class(self, target_name):
        for pokemon_class in self.POKE_LIST:
            if pokemon_class.__name__ == target_name:
                return pokemon_class
        return None
    
    #Timecomplexity is O(n * Comp==) best case and O(n^2 * Comp==) for worst case. Where n is the pokemon classes.
    def choose_manually(self):
        print("a")
        team_size = int(input("Please select the size of your team between 1-6\n"))
        print("b")
        for i in range(team_size):
            try:
                target_name = str(input("Please enter the Pokemon you want to add to your team, example Zapdos:\n"))
            except ValueError:
                print("Please enter a string")
                continue
            pokemon_class = self.find_pokemon_class(target_name)
            self.team[i] = pokemon_class


    def choose_randomly(self) -> None:
        all_pokemon = get_all_pokemon_types()
        self.team_count = 0
        for i in range(self.TEAM_LIMIT):
            rand_int = random.randint(0, len(all_pokemon)-1)
            self.team[i] = all_pokemon[rand_int]()
            self.team_count += 1

    def regenerate_team(self, battle_mode: BattleMode, criterion: str = None) -> None:
        for j in range(self.TEAM_LIMIT):
            pokemon = self.team[j]
            if pokemon: # Check if there is a Pokemon object at this index
                full_health_class = self.find_pokemon_class(pokemon.__class__.__name__)
            if full_health_class:
            # Update the health to the full health as defined in the class
                pokemon.health = full_health_class().health

    def assign_team(self, criterion: str = None) -> None:
        raise NotImplementedError

    def assemble_team(self, battle_mode: BattleMode) -> None:
        raise NotImplementedError

    def special(self, battle_mode: BattleMode) -> None:
        raise NotImplementedError

    def __getitem__(self, index: int):
        """ Returns the object in position index.
        :complexity: O(1)
        :pre: index in between 0 and length - self.array[] checks it
        """
        return self.team[index]

    def __len__(self):
        """ Returns the length of the array
        :complexity: O(1)
        """
        return len(self.team)

    def __str__(self):
        ret_str = "["
        for i, item in enumerate(self.team):
            ret_str += str(item)
            ret_str += ", "
        
        ret_str = ret_str[:-2] + "]"
        return ret_str

class Trainer:

    def __init__(self, name) -> None:
        self.name = name
        self.team = PokeTeam()
        self.pokedox = ArraySet()


    def pick_team(self, method: str) -> None:
        if method == "manual":
            self.team.choose_manually()
        elif method == "random":
            self.team.choose_randomly()
        else:
            raise ValueError("Unknown method")

    def get_team(self) -> PokeTeam:
        return self.team

    def get_name(self) -> str:
        return self.name

    def register_pokemon(self, pokemon: Pokemon) -> None:
        raise NotImplementedError

    def get_pokedex_completion(self) -> float:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError


'''
if __name__ == '__main__':
    t = Trainer('Ash')
    print(t)
    t.pick_team("Random")
    print(t)
    print(t.get_team())
'''


team = PokeTeam()
team.choose_manually()
print(team)
team.regenerate_team()

