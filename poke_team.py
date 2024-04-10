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
        self.descending = False

#How to find pokemon in pokeType.
    #Timecomplexity is O(Comp==) best case and O(n * Comp==) for worst case. Where n is the pokemon classes.
    def find_pokemon_class(self, target_name):
        '''
        This function returns searches the Pokelist for the pokemon class.

        Arguments:
        target_name the name of the pokemon to search for.

        Time complexity:
        best case: O(comp==)
        worst case: O(n * Comp==)
        n is pokemon

        Returns:
        Pokemon Class 
        None
        '''
        for pokemon_class in self.POKE_LIST:
            if pokemon_class.__name__ == target_name:
                return pokemon_class
        return None

    #Timecomplexity is O(n * Comp==) best case and O(n^2 * Comp==) for worst case. Where n is the pokemon classes.
    def choose_manually(self):
        '''
        This function allows the user to populate the team with pokemons through user input.

        Time complexity:
        best case:O(n * comp==) if team size is 1.
        worst case:O(n^2 comp==)\
        n is the number of pokemon classes.


        Returns:
        None
        '''
        team_size = int(input("Please select the size of your team between 1-6\n"))
        for i in range(team_size):
            try:
                target_name = str(input("Please enter the Pokemon you want to add to your team, example Zapdos:\n"))
            except ValueError:
                print("Please enter a string")
                continue
            pokemon_class = self.find_pokemon_class(target_name)    #O(n)
            self.team[i] = pokemon_class()
            self.team_count += 1


    def choose_randomly(self) -> None:
        '''
        This function populates the team randomly according to the team limit.

        Time complexity:
        best case:  O(n)   as we always go through 6 times due to team limit.
        worst case: O(n^2) we go through pokelist inside the for loop too.
        n = pokemons in pokelist.

        Returns:
        The winning pokemon team.
        None
        '''
        all_pokemon = get_all_pokemon_types()
        self.team_count = 0
        for i in range(self.TEAM_LIMIT):
            rand_int = random.randint(0, len(all_pokemon)-1)
            self.team[i] = all_pokemon[rand_int]()  #all_pokemon has size n of pokemons. O(n)
            self.team_count += 1

    def regenerate_team(self, battle_mode: BattleMode, criterion: str = None) -> None:
        '''
        This function will regenerate pokemons in the team back to full hp according to the battle mode selected.
        Each team will have a different data structure most suitable for each battle mode.

        Arguments:
        BattleMode: the selecected battle mode.
        criterion: the selected criteria.

        Time complexity:
        best case:  O(n^2 * comp==)
        worst case: #O(n^2 log(n) * comp==) Optimised mode is chosen

        Returns:
        None. sets health of existing team to full.
        '''
        if(battle_mode == BattleMode.OPTIMISE): #O(n^2 log(n) * comp==)
            for j in range(self.TEAM_LIMIT):
                pokemon = self.team[j]
                if pokemon: # Check if there is a Pokemon object at this index
                    full_health_class = self.find_pokemon_class(pokemon.value.__class__.__name__) #O(n)
                if full_health_class:
                # Update the health to the full health as defined in the class
                    pokemon.value.health = full_health_class().health

            self.temp_team = ArrayR(self.TEAM_LIMIT)
            for j in range(len(self)):                  #O(n)
                self.temp_team[j] = self.team[j].value
            self.team = self.temp_team
            self.assemble_team(battle_mode)     #O(n * comp==)
            self.assign_team(criterion)
        else:
            for j in range(self.TEAM_LIMIT):        #O(n)
                pokemon = self.team[j]
                if pokemon: # Check if there is a Pokemon object at this index
                    full_health_class = self.find_pokemon_class(pokemon.__class__.__name__) #O(n * comp==)
                if full_health_class:
                # Update the health to the full health as defined in the class
                    pokemon.health = full_health_class().health
            self.assemble_team(battle_mode)     #O(n)


    #This function assigns the order of the team based on the criterion list.
    def assign_team(self, criterion: str = None) -> None:
        '''
        This function assigns the team order based on the criteria chosen example "health".

        Arguments:
        criterion: the selected criteria is inputed as a string.

        Time complexity:
        best case:O(1)
        worst case:O(n)
        n is pokemon in team

        Returns:
        None. Sorts the team according to critria chosen.
        '''
        #Created a new temporary list for the team.
        temp_list = ArraySortedList(self.TEAM_LIMIT)
        for j in range(self.team_count):        #O(n)
            pokemon = self.team[j]
            key = pokemon.value.get__attribute__by__criteria(criterion) #method made in pokemon_base.py O(comp==)
            temp_list.add(ListItem(key=key, value=pokemon.value))
        # Clear the current team to repopulate it
        self.team.reset()

        # Add each ListItem back to the team, now sorted by the new criterion
        for j in range(self.team_count):
            self.team.add(temp_list[j])

    #This function assembles the team based on the battle_mode selected.
    #Each battle_mode has different data structures.
    def assemble_team(self, battle_mode: BattleMode) -> None:
        '''
        This function assembles three different data structures most suitable for each battle_mode.
        The three data structures are Stack, Circular-Queue and an Array Sorted List.
        
        Arguments:
        battle_mode: the selected battle mode.

        Time complexity:
        best case: O(comp== * n)
        worst case: O(comp== * n^2 log n)  when optimised mode is run
        n is team limit.

        Returns:
        None. Changes the existing team data structure.
        '''
        if battle_mode == BattleMode.SET:               #O(Comp==)
            temp_team = ArrayStack(self.TEAM_LIMIT)
            # Add each Pokémon in self.team to the stack
            for pokemon in range(len(self.team)):       #len = O(1)     for loop O(n) n = team limit.
                temp_team.push(self.team[pokemon])      #push() = O(1)

            self.team = temp_team.copy()                #O(n) added to the stack adt.
        elif battle_mode == BattleMode.ROTATE:          #O(comp==)
            circular_queue = CircularQueue(self.TEAM_LIMIT)
            # Add each Pokémon in self.team to the circular queue
            for pokemon in self.team:                   #O(n)
                circular_queue.append(pokemon)          #append() = O(1)
            self.team = circular_queue
        #Optimised Mode
        elif battle_mode == BattleMode.OPTIMISE:        #O(comp==)
            sorted_list = ArraySortedList(self.TEAM_LIMIT)

            for pokemon in self.team:                   #O(n)
                key = pokemon.get__attribute__by__criteria('health')    #O(comp==)
                sorted_list.add(ListItem(key=key, value=pokemon))       #add() = O(nlog(n))
            self.team = sorted_list


    #SET Mode Reverses the first half of the team
    #Rotate Mode reverses the second half of the team
    #Optimise mode it reverses the other, either ascending to descending or descending to ascending order.
    def special(self, battle_mode: BattleMode) -> None:
        '''
        This function peforms a change in the order of the pokemon within the team. Each battle mode has a different order.
        SET mode reverses the first half of the team.
        Rotate mode reverses the second half of the team.
        Optimise mode it reverses the order of the team, either ascending to descending or descending to ascending order each time special is called.
        

        Time complexity:
        best case: O(comp==) if mode chosen is manual with 1 pokemon in team
        worst case: O(nlog(n) * comp==)
        n = team size

        Returns:
        The winning pokemon team.
        None
        '''
        if battle_mode == BattleMode.SET:           #O(n*comp=)
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

        elif battle_mode == BattleMode.ROTATE:      #O(n*comp==)
            q_length = len(self.team)
            half_point = q_length // 2

            first_half_size = half_point
            second_half_size = q_length - half_point

            first_half = ArrayR(first_half_size)
            second_half = ArrayR(second_half_size)

            for i in range(first_half_size):
                first_half[i] = self.team.serve()

            for i in range(second_half_size):
                second_half[i] = self.team.serve()

            for i in range(first_half_size):
                self.team.append(first_half[i])

            for i in range(second_half_size-1,-1,-1):
                self.team.append(second_half[i])

        elif battle_mode == BattleMode.OPTIMISE:    #O(n*log(n) * comp==)
            self.descending = not self.descending
            temp_list = ArraySortedList(self.TEAM_LIMIT, self.descending)

            for i in range(len(self.team)):
                temp_list.add(self.team[i])

            self.team = temp_list


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
        return min(self.TEAM_LIMIT,len(self.team))

    def __str__(self):
        '''
        This function returns a string representation of the team based on the data structure of the team.

        Time complexity:
        best case:O(isinstance * n)
        worst case: O(isinstance * n)
        n = pokemon in team.

        Returns:
        The winning pokemon team.
        None
        '''
        ret_str = "["
        if isinstance(self.team, ArrayStack):
            for i in range(len(self.team.array)):
                ret_str += "(" + str(self.team.array[i]) + "), \n"
        elif isinstance(self.team, ArraySortedList):
            for i in range(len(self.team.array)):
                ret_str += "(" + str(self.team.array[i]) + "), \n "
        elif isinstance(self.team, CircularQueue):
            for i in range(len(self.team.array)):
                ret_str += "(" + str(self.team.array[i]) + "), \n"
        else:
            # Handle other cases here
            # Handle other cases here
            for j in range(len(self)):
                ret_str += "(" + str(self.team[j]) + "),\n"
            ret_str = ret_str[:-2] # Remove the trailing comma and space

        if ret_str.endswith(", "):
            ret_str = ret_str[:-2]  # Remove the trailing comma and space
        ret_str += "]"
        return ret_str

class Trainer:

    def __init__(self, name) -> None:
        self.name = name
        self.team = PokeTeam()
        self.pokedox = ArraySet()


    def pick_team(self, method: str) -> None:
        '''
        This function selects the team to be selected either randomly or manually through a sting arguement.
        The method also registers the pokemon selected either randomly or manually.

        Arguments:
        method: the method to be used to select the team. A string of the method either Manual or Random.

        Time complexity:
        best case:
        worst case:

        Returns:
        None.
        '''
        if method == "Manual":
            self.team.choose_manually()
        elif method == 'Random':
            self.team.choose_randomly()
        else:
            raise ValueError("Unknown method")
        for j in range(len(self.team)):
            self.register_pokemon(self.team[j])

    def get_team(self) -> PokeTeam:
        '''
        This function retuns the team.

        Time complexity:
        best case: O(1)
        worst case: O(1)

        Returns:
        the team.
        '''
        
        return self.team

    def get_name(self) -> str:
        '''
        This function returns the name of the trainer.

        Time complexity:
        best case: O(1)
        worst case: O(1)

        Returns:
        Name of the trainer as a string.
        '''
        return self.name

    def register_pokemon(self, pokemon: Pokemon) -> None:
        '''
        This function register pokemon within the assembled team through a for loop. It uses the add method within stack to prevent duplicates.

        Arguments:
        pokemon: the pokemon to be registered within the team (object).

        Time complexity:
        best case: O(1)
        worst case: O(n)
        n = pokemon in pokemonclass.

        Returns:
        None
        '''
        pokemon_type = pokemon.get_poketype()
        if pokemon_type not in self.pokedox:
            self.pokedox.add(pokemon_type)


    def get_pokedex_completion(self) -> float:
        '''
        This function returns a float value rounded to 2 decimal place of the Pokedex completion.

        Time complexity:
        best case:  O(1)
        worst case: O(1)

        Returns:
        rounded float value for Pokedex completion.
        '''
        poke_types_stored = len(self.pokedox)
        maximum_size_of_pokedex = len(PokeType)

        return round((poke_types_stored/maximum_size_of_pokedex), 2 )

    def __str__(self) -> str:
        '''
        Method returns the trainer name and pokedex completion percentage as a string.

        Time complexity:
        best case: O(1)
        worst case: O(1)

        Returns:
        String of the trainer name and pokedex completion percentage.
        '''
        precent_completion = int(self.get_pokedex_completion() * 100)
        return f"Trainer {self.name} Pokedex Completion: {precent_completion}%"

	

if __name__ == '__main__':
    t = Trainer('Ash')
    print(t)
    t.pick_team("Random")
    print(t)
    print(t.get_team())




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
trainer.register_pokemon(Pikachu())
print("Pokédex after registering Pikachu:", trainer.pokedox)
print(trainer.get_pokedex_completion())
'''

'''
#circular que. Test.
team = PokeTeam()
print(team)
print("\n")
team.choose_randomly()
print(team)
print("\n")
team.assemble_team(BattleMode.ROTATE)
print(team)
team.special(BattleMode.ROTATE)
print("\n")
print(team)`
'''


'''	
#Optimised Mode testing
team = PokeTeam()
print(team)
print("\n")
team.choose_randomly()
print(team)
print("\n")
print('Assembled Team')
team.assemble_team(BattleMode.OPTIMISE)

team.assign_team('health')
print(team)

team.special(BattleMode.OPTIMISE) #ascending order
print("\n")
print(team)

team.special(BattleMode.OPTIMISE) #descending order
print("\n")
print(team)
'''	

'''
#SET Mode testing
team = PokeTeam()
team.choose_randomly()
print(team)
print("\n")
team.assemble_team(BattleMode.SET)
print(team)
print("\n")
team.special(BattleMode.SET)
print(team)
print("\n")
team.special(BattleMode.SET)
print(team)
'''


