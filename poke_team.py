from pokemon import *
import random
from typing import List
from battle_mode import BattleMode
from data_structures.referential_array import *
from data_structures.set_adt import *
from data_structures.stack_adt import *
from data_structures.queue_adt import *
from data_structures.array_sorted_list import *


class ArraySet(Set[T]):
    #Time complexity O(n * Comp==) best case is O(Comp==)
    MIN_CAPACITY = 1
    def __init__(self, capacity: int = 15) -> None:
        Set.__init__(self)
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
    
    #time complexity is O(N*Comp==) where N is the size of set. best case is O(1).
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
        
    def __str__(self):
        return ", ".join(str(item) for item in self.array if item is not None)
    
    #time complexity is O(N * Comp==) and best case is O(1).
    def add(self, item: T) -> None:
        if item not in self:
            if self.is_full():
                raise Exception("Set is full")
        self.array[self.size] = item
        self.size += 1
        
    def union(self, other: Set[T]) -> Set[T]:
        """ Makes a union of the set with another set. """
        pass

    def intersection(self, other: Set[T]) -> Set[T]:
        """ Makes an intersection of the set with another set. """
        pass

    def difference(self, other: Set[T]) -> Set[T]:
        """ Creates a difference of the set with another set. """
        pass

    

class PokeTeam:
    TEAM_LIMIT = 6
    POKE_LIST = get_all_pokemon_types()
    CRITERION_LIST = ["health", "defence", "battle_power", "speed", "level"]

    def __init__(self):
        self.team = ArrayR(self.TEAM_LIMIT)
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
        team_size = int(input("Please select the size of your team between 1-6\n"))
        for i in range(team_size):
            try:
                target_name = str(input("Please enter the Pokemon you want to add to your team, example Zapdos:\n"))
            except ValueError:
                print("Please enter a string")
                continue
            pokemon_class = self.find_pokemon_class(target_name)
            self.team[i] = pokemon_class()
            self.team_count += 1


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
        self.assemble_team(battle_mode)
        if battle_mode == 2:
            self.assign_team(criterion)


    #This function assigns the order of the team based on the criterion list.
    def assign_team(self, criterion: str = None) -> None:
        #Created a new temporary list for the team.
        temp_list = ArraySortedList(self.TEAM_LIMIT)
        for j in range(self.team_count):
            pokemon = self.team[j]
            key = pokemon.get__attribute__by__criteria(criterion)
            temp_list.add(ListItem(key=key, value=pokemon))
        # Clear the current team to repopulate it
        self.team.reset()
        # Add each ListItem back to the team, now sorted by the new criterion
        for j in range(self.team_count):
            self.team.add(temp_list[j])

    #This function assembles the team based on the battle_mode selected.
    #Each battle_mode has different data structures.
    def assemble_team(self, battle_mode: BattleMode) -> None:
        if battle_mode == 0:

            temp_team = ArrayStack(self.TEAM_LIMIT)
            # Add each Pokémon in self.team to the stack
            for pokemon in range(len(self.team)):
                temp_team.push(self.team[pokemon])

            self.team = temp_team.copy()

        elif battle_mode == 1:
            temp_team_2 = CircularQueue(self.TEAM_LIMIT)
            temp = CircularQueue(self.TEAM_LIMIT)
            # Add each Pokémon in self.team to the circular queue
            for pokemon in self.team:
                temp_team_2.append(pokemon)
            temp_team_2.print_items()
            print("\n")
            self.team = CircularQueue(self.TEAM_LIMIT)
            self.team = temp_team_2
            #print(self.team)
        #Optimised Mode
        elif battle_mode == 2:
            self.team = ArraySortedList(self.TEAM_LIMIT)




    #SET Mode Reverses the first half of the team
    #Rotate Mode reverses the second half of the team
    #Optimise mode it reverses the other, either ascending to descending or descending to ascending order.
    def special(self, battle_mode: BattleMode) -> None:
        if battle_mode == 0:
            temp_stack1 = ArrayStack(len(self.team))  
            temp_stack2 = ArrayStack(len(self.team))  

            half_length = len(self.team)// 2

            for _ in range(half_length, len(self.team)):
                temp_stack1.push(self.team.pop())

            while not self.team.is_empty():
                temp_stack2.push(self.team.pop())

            self.team = temp_stack2.copy()

            while not temp_stack1.is_empty():
                self.team.push(temp_stack1.pop())

        elif battle_mode == 1:
            q_length = len(self.team)   #q length example 6
            half_point = q_length // 2  #half point example 3

            first_half_size = half_point            #first half size = 3
            second_half_size = q_length - half_point    #6-3 example

            first_half = ArrayR(first_half_size)        #first half array
            second_half = ArrayR(second_half_size)      #second half array

            for i in range(first_half_size):        
                first_half[i] = self.team.serve()       #serves first half [1,2,3] example

            for i in range(second_half_size):       #serves second half [4,5,6]
                second_half[i] = self.team.serve()

            for i in range(first_half_size):        
                self.team.append(first_half[i])     #self.team = [1,2,3]

            for i in range(second_half_size-1,-1,-1): # itterate second hal array [4,5,6] in reverse order.
                self.team.append(second_half[i])      # final will be [1,2,3,6,5,4]
            
        elif battle_mode == 2:
            pass


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

    '''
    def __str__(self):
        ret_str = "["
        for i, item in enumerate(self.team):
            ret_str += str(item)
            ret_str += ", "
        ret_str = ret_str[:-2] + "]"
        return ret_str
    '''
    ''''''
    def __str__(self):
        ret_str = "["
        if isinstance(self.team, ArrayStack):
            temp_stack = self.team.copy()
            for j in range(len(self.team)):
                pokemon = temp_stack.pop()
                ret_str += "(" + str(pokemon) + "), \n "
        elif isinstance(self.team, ArraySortedList):
            for i in range(len(self.team.array)):
                ret_str += "(" + str(self.team.array[i]) + "), "
        elif isinstance(self.team, CircularQueue):
            for i in range(len(self.team.array)):
                ret_str += "(" + str(self.team.array[i]) + "),\n "
        else:
            # Handle other cases here
            for pokemon in self.team:
                ret_str += "(" + str(pokemon) + "),\n"
            ret_str = ret_str[:-2]  # Remove the trailing comma and space
            

        
        return ret_str + "]"




class Trainer:

    def __init__(self, name) -> None:
        self.name = name
        self.team = PokeTeam()
        self.pokedox = ArraySet()


    def pick_team(self, method: str) -> None:
        if method == "Manual":
            self.team.choose_manually()
        elif method == 'Random':
            self.team.choose_randomly()
        else:
            raise ValueError("Unknown method")

    def get_team(self) -> PokeTeam:
        return self.team

    def get_name(self) -> str:
        return self.name

    def register_pokemon(self, pokemon: Pokemon) -> None:
        pokemon_type = pokemon.get_poketype()
        if pokemon_type not in self.pokedox:
            self.pokedox.add(pokemon_type)


    def get_pokedex_completion(self) -> float:
        poke_types_stored = len(self.pokedox)
        maximum_size_of_pokedex = len(PokeType)

        return round((poke_types_stored/maximum_size_of_pokedex), 2 )

    def __str__(self) -> str:
        precent_completion = int(self.get_pokedex_completion() * 100)
        return f"Trainer {self.name} Pokedex Completion: {precent_completion}%"


"""	
if __name__ == '__main__':
    t = Trainer('Ash')
    print(t)
    t.pick_team("Random")
    print(t)
    print(t.get_team())
    
"""	

"""	
Bug fixes for optimised mode

team = PokeTeam()
team.assemble_team(2)
team.choose_randomly()
print(team)
print("\n")
team.assign_team("health")
print(team)
"""

'''	

Bug fixes for registering pokemon in pokedex.

trainer = Trainer('Ash')
print(trainer)

# Register Pokémon and print the Pokédex after each registration
trainer.register_pokemon(Pikachu())
print("Pokédex after registering Pikachu:", trainer.pokedox)
trainer.register_pokemon(Pidgey())
print("Pokédex after registering Pidgey:", trainer.pokedox)
trainer.register_pokemon(Aerodactyl())
print("Pokédex after registering Aerodactyl:", trainer.pokedox)
trainer.register_pokemon(Squirtle())
print("Pokédex after registering Squirtle:", trainer.pokedox)
trainer.register_pokemon(Weedle())
print("Pokédex after registering Weedle:", trainer.pokedox)
trainer.register_pokemon(Meowth())
print("Pokédex after registering Meowth:", trainer.pokedox)
trainer.register_pokemon(Zapdos())
print("Pokédex after registering Zapdos:", trainer.pokedox)
print(trainer)

'''

#circular que.
team = PokeTeam()
print(team)
print("\n")
team.choose_randomly()
print(team)
print("\n")
team.assemble_team(1)
print(team)
print("\n")
team.special(1)
print(team)




'''
#array_stack testing
team = PokeTeam()
print(team)
print("\n")
team.choose_randomly()
print(team)
print("\n")
team.assemble_team(0)
print(team)

print("\n")
print(len(team))

team.special(0)
print("\n")
print(team)
'''
