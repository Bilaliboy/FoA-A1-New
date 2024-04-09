from __future__ import annotations
from poke_team import *
from typing import Tuple
from battle_mode import BattleMode


class Battle:
    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion = "health") -> None:
        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2
        self.battle_mode = battle_mode
        self.criterion = criterion
        random.seed(20)

    def commence_battle(self) -> Trainer | None:
        '''
        Each battle mode already retuns a winner or none if its draw.
        This function will be called to start the battle and will return the outcome of the battle.
        '''
        if self.battle_mode == BattleMode.SET:
            result = self.set_battle()
            if result == self.trainer_1.team.team:
                return self.trainer_1
            elif result == self.trainer_2.team.team:
                return self.trainer_2
            else:
                return None
        elif self.battle_mode == BattleMode.ROTATE:
            result = self.rotate_battle()
            if result == self.trainer_1.team.team:
                return self.trainer_1
            elif result == self.trainer_2.team.team:
                return self.trainer_2
            else:
                return None
        elif self.battle_mode == BattleMode.OPTIMISE:
            result = self.optimise_battle()
            if result == self.trainer_1.team.team:
                return self.trainer_1
            elif result == self.trainer_2.team.team:
                return self.trainer_2
            else:
                return None

    def perform_battle(self, pokemon1: Pokemon, pokemon2: Pokemon) -> None:
    # If P1 speed is greater than P2
        if pokemon1.get_speed() > pokemon2.get_speed():
            #print(f"{pokemon1.name} attacks against {pokemon2.name}")
            damage = ceil(pokemon1.attack(pokemon2)) * (self.trainer_1.get_pokedex_completion()/self.trainer_2.get_pokedex_completion())
            #print(f"{pokemon1.name} damage = {damage}")
            pokemon2.defend(damage)
            #print(f"{pokemon2.name} health after attack = {pokemon2.get_health()}")
            if pokemon2.is_alive():
                #print(f"{pokemon2.name} counter attacks {pokemon1.name}")
                counter_damage_to_p1 = ceil(pokemon2.attack(pokemon1)) * (self.trainer_2.get_pokedex_completion()/self.trainer_1.get_pokedex_completion())  # If still alive, P2 attacks P1
                #print(f"{pokemon2.name} counter damage = {counter_damage_to_p1}")
                pokemon1.defend(counter_damage_to_p1)
                #print(f"{pokemon1.name} health after counter attack = {pokemon1.get_health()}")
        # If P2 speed is greater than P1
        elif pokemon1.get_speed() < pokemon2.get_speed():
            #print(f"{pokemon2.name} attacks against {pokemon1.name}")
            damage = ceil(pokemon2.attack(pokemon1)) * (self.trainer_2.get_pokedex_completion()/self.trainer_1.get_pokedex_completion())
            #print(f"{pokemon2.name} damage = {damage}")
            pokemon1.defend(damage)
            #print(f"{pokemon1.name} health after attack = {pokemon1.get_health()}")
            if pokemon1.is_alive():
                #print(f"{pokemon1.name} counter attacks {pokemon2.name}")
                counter_damage_to_p2 = ceil(pokemon1.attack(pokemon2)) * (self.trainer_1.get_pokedex_completion()/self.trainer_2.get_pokedex_completion())  # If still alive, P1 attacks P2
                #print(f"{pokemon1.name} counter damage = {counter_damage_to_p2}")
                pokemon2.defend(counter_damage_to_p2)
                #print(f"{pokemon2.name} health after counter attack = {pokemon2.get_health()}")
        else:
            # Perform simultaneous attacks if speed is the same
            #print(f"{pokemon1.name} and {pokemon2.name} both launch attacks!")
            damage_to_p2 = ceil(pokemon1.attack(pokemon2)) * (self.trainer_1.get_pokedex_completion()/self.trainer_2.get_pokedex_completion())
            #print(f"{pokemon1.name} damage against {pokemon2.name} = {damage_to_p2}")
            damage_to_p1 = ceil(pokemon2.attack(pokemon1)) * (self.trainer_2.get_pokedex_completion()/self.trainer_1.get_pokedex_completion())
            #print(f"{pokemon2.name} damage agains {pokemon1.name} = {damage_to_p1}")
            pokemon1.defend(damage_to_p1)
            #print(f"{pokemon1.name} health after attack = {pokemon1.get_health()}")
            pokemon2.defend(damage_to_p2)
            #print(f"{pokemon2.name} health after attack = {pokemon2.get_health()}")


    def _create_teams(self) -> None:
        if self.battle_mode == BattleMode.SET:
            self.trainer_1.pick_team("Random")
            self.trainer_2.pick_team("Random")
            self.trainer_1.team.assemble_team(BattleMode.SET)
            self.trainer_2.team.assemble_team(BattleMode.SET)

        elif self.battle_mode == BattleMode.ROTATE:
            self.trainer_1.pick_team("Random")
            self.trainer_2.pick_team("Random")
            self.trainer_1.team.assemble_team(BattleMode.ROTATE)
            self.trainer_2.team.assemble_team(BattleMode.ROTATE)

        elif self.battle_mode == BattleMode.OPTIMISE:
            self.trainer_1.pick_team("Random")
            self.trainer_2.pick_team("Random")
            self.trainer_1.team.assemble_team(BattleMode.OPTIMISE)
            self.trainer_2.team.assemble_team(BattleMode.OPTIMISE)
            self.trainer_1.team.assemble_team(self.criterion)
            self.trainer_2.team.assemble_team(self.criterion)


        '''
        if You want to change the criteria with user inputs did not know we were not supposed to do this.

        #Trainer 1 picks team randomly or manually
        while True:
            #Validate to make sure they pick a team.
            try:
                trainer_1_pick = int(input("Pick your team trainer 1:\n Random (1) \n Manual (2) \n Enter corresponding number: "))
                if trainer_1_pick == 1 or trainer_1_pick == 2:
                    break  # Exit the loop if input is valid
                else:
                    print("Please enter either 1 or 2")
            except ValueError:
                print("Please enter a number (1 or 2)")

        #Trainer 2 picks team randomly or manually
        while True:
            #Validate to make sure they pick a team.
            try:
                trainer_2_pick = int(input("Pick your team trainer 2:\n Random (1) \n Manual (2) \n Enter corresponding number: "))
                if trainer_2_pick == 1 or trainer_2_pick == 2:
                    break  # Exit the loop if input is valid
                else:
                    print("Please enter either 1 or 2")
            except ValueError:
                print("Please enter a number (1 or 2)")

        #If trainer 1 picks random method
        if trainer_1_pick == 1:
            self.trainer_1.pick_team("Random")

            #Assemble the team based on battle mode selected. Check for battle Mode selected.
            if self.battle_mode == BattleMode.SET:
                self.trainer_1.team.assemble_team(battle_mode=BattleMode.SET)
            elif self.battle_mode == BattleMode.ROTATE:
                self.trainer_1.team.assemble_team(battle_mode=BattleMode.ROTATE)
            elif self.battle_mode == BattleMode.OPTIMISE:
                try:
                    #asks user to select a criteria.
                    criteria = str(input("Team 1, please type in a criteria to sort the team by\n health, defence, battle_power, speed, level:\n"))    #Input for criteria selection
                except ValueError:
                    print("Please enter a string")
                self.trainer_1.team.assemble_team(battle_mode=BattleMode.OPTIMISE)
                self.trainer_1.team.assign_team(criteria)   #Assign team based on criteria selected

        #If trainer 1 picks manual method
        elif trainer_1_pick == 2:
            self.trainer_1.pick_team("Manual")
            #Assemble the team based on battle mode selected. Check for battle Mode selected.
            if self.battle_mode == BattleMode.SET:
                self.trainer_1.team.assemble_team(battle_mode=BattleMode.SET)
            elif self.battle_mode == BattleMode.ROTATE:
                self.trainer_1.team.assemble_team(battle_mode=BattleMode.ROTATE)
            elif self.battle_mode == BattleMode.OPTIMISE:
                try:
                    #asks user to select a criteria.
                    criteria = str(input("Team 1, please select a criteria to sort the team by\n health, defence, battle_power, speed, level:\n"))    #Input for criteria selection
                except ValueError:
                    print("Please enter a string")
                self.trainer_1.team.assemble_team(battle_mode=BattleMode.OPTIMISE)
                self.trainer_1.team.assign_team(criteria)   #Assign team based on criteria selected

        #If trainer 2 picks random method.
        if trainer_2_pick == 1:
            self.trainer_2.pick_team("Random")

            #Assemble the team based on battle mode selected. Check for battle Mode selected.
            if self.battle_mode == BattleMode.SET:
                self.trainer_2.team.assemble_team(battle_mode=BattleMode.SET)
            elif self.battle_mode == BattleMode.ROTATE:
                self.trainer_2.team.assemble_team(battle_mode=BattleMode.ROTATE)
            elif self.battle_mode == BattleMode.OPTIMISE:
                try:
                    #asks user to select a criteria.
                    criteria = str(input("Team 2, please select a criteria to sort the team by\n health, defence, battle_power, speed, level:\n"))    #Input for criteria selection
                except ValueError:
                    print("Please enter a string")
                self.trainer_2.team.assemble_team(battle_mode=BattleMode.OPTIMISE)
                self.trainer_2.team.assign_team(criteria)   #Assign team based on criteria selected

        #If trainer 2 picks Manual method.
        elif trainer_2_pick == 2:
            self.trainer_2.pick_team("Manual")
            #Assemble the team based on battle mode selected. Check for battle Mode selected.
            if self.battle_mode == BattleMode.SET:
                self.trainer_2.team.assemble_team(battle_mode=BattleMode.SET)
            elif self.battle_mode == BattleMode.ROTATE:
                self.trainer_2.team.assemble_team(battle_mode=BattleMode.ROTATE)
            elif self.battle_mode == BattleMode.OPTIMISE:
                try:
                    #asks user to select a criteria.
                    criteria = str(input("Team 2, please select a criteria to sort the team by\n health, defence, battle_power, speed, level:\n"))    #Input for criteria selection
                except ValueError:
                    print("Please enter a string")
                self.trainer_2.team.assemble_team(battle_mode=BattleMode.OPTIMISE)
                self.trainer_2.team.assign_team(criteria)   #Assign team based on criteria selected
        '''

    # Note: These are here for your convenience
    # If you prefer you can ignore them

    #This function will use a stack as the last pokemon selected is the first pokemon battling.
    def set_battle(self) -> PokeTeam | None:
        #Then Store the pokemon at the top as another variable example pokemon_1 and pokemon_2.
        #then we go through the battle logic:
        #First we compare the speed of the pokemons and complete the battle phase for the faster pokemon against slower pokemon.
        #If both pokemons

        print(self.trainer_1.get_team())
        print(self.trainer_2.get_team())
        self.dead_pokemon_1 = ArrayStack(6)  #Empty stack for dead pokemon
        self.dead_pokemon_2 = ArrayStack(6)  #Empty Stack for dead pokemon

        while True:
            pokemon1 = self.trainer_1.team.team.pop() #Pokemon fighting in trainer_1's team
            pokemon2 = self.trainer_2.team.team.pop() #Pokemon fighting in trainer 2's team
            self.trainer_1.register_pokemon(pokemon2)
            self.trainer_2.register_pokemon(pokemon1)

            #Battle logic
            self.perform_battle(pokemon1,pokemon2)

            #If the attacker (pokemon 1) is still alive and the defender (pokemon 2) is dead, then attacker (pokemon 1) lvls up and remains battling.
            if pokemon1.is_alive() and not pokemon2.is_alive():
                print("pokemon1 alive, pokemon2 dead")
                pokemon1.level_up()
                self.dead_pokemon_2.push(pokemon2)     #pokemon 2 added to dead stack
                self.trainer_1.team.team.push(pokemon1)

            #If the attacker (pokemon 2) is still alive and the defender (pokemon 1) is dead, then attacker (pokemon 2) lvls up and remains battling.
            elif pokemon2.is_alive() and not pokemon1.is_alive():
                print("pokemon1 dead, pokemon2 alive")
                pokemon2.level_up()
                self.dead_pokemon_1.push(pokemon1)     #Pokemon 1 added to dead stack
                self.trainer_2.team.team.push(pokemon2)

            #If both pokemon1 and pokemon2 are alive after the battle phase, then both take 1 damage.
            else:
                pokemon1.health -=1 #pokemon1.health -=1
                pokemon2.health -=1 #pokemon2.health -=1

                #Covers the cases after they both take 1 damage.
                if pokemon1.is_alive() and pokemon2.is_alive():     #Continue fighting
                    self.trainer_1.team.team.push(pokemon1)
                    self.trainer_2.team.team.push(pokemon2)

                elif pokemon1.is_alive() and not pokemon2.is_alive():
                    pokemon1.level_up()
                    self.dead_pokemon_2.push(pokemon2)     #pokemon 2 added to dead stack
                    self.trainer_1.team.team.push(pokemon1)

                elif pokemon2.is_alive() and not pokemon1.is_alive():
                    pokemon2.level_up()
                    self.dead_pokemon_1.push(pokemon1)     #Pokemon 1 added to dead stack
                    self.trainer_2.team.team.push(pokemon2)

                elif not(pokemon1.is_alive() and pokemon2.is_alive()):
                    #Both pokemon have fainted added to dead stack.
                    self.dead_pokemon_1.push(pokemon1)
                    self.dead_pokemon_2.push(pokemon2)


            print(self.trainer_1.get_team())
            print(self.trainer_2.get_team())
            if self.trainer_1.team.team.is_empty():
                print(f"team 1 is empty if true: {self.trainer_1.team.team.is_empty()}")
                break
            elif self.trainer_2.team.team.is_empty():
                print(f"team 2 is empty if true: {self.trainer_2.team.team.is_empty()}")
                break

        print("out of loop")
            # Determine the winner
        if self.trainer_1.team.team.is_empty():
            print("winner team 2")
            return self.trainer_2.team.team
        elif self.trainer_2.team.team.is_empty():
            print("winner team 1")
            return self.trainer_1.team.team
        else:
            return None

    #This function will use a circular Queue implementation as the each pokemon is sent back to the end of the battle queue after
    #each pokemon battle.
    def rotate_battle(self) -> PokeTeam | None:

        print("team 1 before battle")
        self.trainer_1.get_team().team.print_items()
        print("team 2 before battle")
        self.trainer_2.get_team().team.print_items()

        self.dead_pokemon_1 = CircularQueue(6) #Empty queue to store dead pokemon from team 1 to add back later
        self.dead_pokemon_2 = CircularQueue(6) #Empty queue to store dead pokemon from team 2 to add back later

        while not self.trainer_1.team.team.is_empty() and not self.trainer_2.team.team.is_empty():
            # serve the first Pokémon of each team for the battle
            pokemon1 = self.trainer_1.team.team.serve()
            pokemon2 = self.trainer_2.team.team.serve()

            # Register the Pokémons
            self.trainer_1.register_pokemon(pokemon2)
            self.trainer_2.register_pokemon(pokemon1)

            # Battle Logic
            self.perform_battle(pokemon1, pokemon2)

            # Check for fainting
            # If the attacker (pokemon 1) is still alive and the defender (pokemon 2) is dead
            if pokemon1.is_alive() and not pokemon2.is_alive():
                pokemon1.level_up()
                self.trainer_1.team.team.append(pokemon1)
                self.dead_pokemon_2.append(pokemon2)
            # If the attacker (pokemon 2) is still alive and the defender (pokemon 1) is dead
            elif pokemon2.is_alive() and not pokemon1.is_alive():
                pokemon2.level_up()
                self.trainer_2.team.team.append(pokemon2)
                self.dead_pokemon_1.append(pokemon1)
            # If both pokemon1 and pokemon2 are alive after the battle phase, then both take 1 damage.
            else:
                pokemon1.defend(1)
                pokemon2.defend(1)
                # Add pokemons back to respective teams or dead queues accordingly
                if pokemon1.is_alive() and pokemon2.is_alive():
                    self.trainer_1.team.team.append(pokemon1)
                    self.trainer_2.team.team.append(pokemon2)
                elif pokemon1.is_alive() and not pokemon2.is_alive():
                    self.trainer_1.team.team.append(pokemon1)
                    self.dead_pokemon_2.append(pokemon2)
                elif pokemon2.is_alive() and not pokemon1.is_alive():
                    self.trainer_2.team.team.append(pokemon2)
                    self.dead_pokemon_1.append(pokemon1)
                else:
                    self.dead_pokemon_1.append(pokemon1)
                    self.dead_pokemon_2.append(pokemon2)

        print("team 1 after battle")
        self.trainer_1.get_team().team.print_items()
        print("team 2 after battle")
        self.trainer_2.get_team().team.print_items()

        # Determine the winner after the battle loop
        if self.trainer_1.team.team.is_empty():
            return self.trainer_2.team.team
        elif self.trainer_2.team.team.is_empty():
            return self.trainer_1.team.team
        else:
            return None

    #In the optimised mode. User picks a stat to order their team.The initial order will be maintained even if a certain stat decreases.
    #The stats are stored in the criterion list in task 2.
    #The assign method in Task 2 assigns the order of the team based on the chosen attribute from the criterion list.
    #therefore i believe using a sorted list is the best method in order to do this task as you can sort the team based on the attribute.
    def optimise_battle(self) -> PokeTeam | None:

        #print("team 1 before battle")
        #self.trainer_1.get_team().team.print_items()
        #print("\n")
        #print("team 2 before battle")
        #self.trainer_2.get_team().team.print_items()

        self.dead_pokemon_1 = ArraySortedList(6) #Empty list to store dead pokemon from team 1 to add back later
        self.dead_pokemon_2 = ArraySortedList(6) #Empty list to store dead pokemon from team 2 to add back later

        while not self.trainer_1.team.team.is_empty() and not self.trainer_2.team.team.is_empty():
            #before we delete at index
            self.trainer_1.get_team().team.print_items()
            print("\n")
            print("team 2 before battle")
            self.trainer_2.get_team().team.print_items()

            pokemon1 = self.trainer_1.team.team.delete_at_index(0)   #removes the first element of the team
            print("\n")
            print(pokemon1)
            pokemon2 = self.trainer_2.team.team.delete_at_index(0)   #removes the first element of the team
            print("\n")
            print(pokemon2)
            print("\n")

            #after we delete at index. problem occurs here.
            print("team 1 before battle")
            self.trainer_1.get_team().team.print_items()
            print("\n")
            print("team 2 before battle")
            self.trainer_2.get_team().team.print_items()

            pokemon1_ListItem = pokemon1
            pokemon2_ListItem = pokemon2
            pokemon1 = pokemon1_ListItem.value
            pokemon2 = pokemon2_ListItem.value

            self.trainer_1.register_pokemon(pokemon2)
            self.trainer_2.register_pokemon(pokemon1)
            #Battle Logic
            self.perform_battle(pokemon1, pokemon2)

            #Check for Fainting
            #If the attacker (pokemon 1) is still alive and the defender (pokemon 2) is dead, then attacker (pokemon 1) lvls up and returns to back of queue.
            if pokemon1.is_alive() and not pokemon2.is_alive():
                pokemon1.level_up()
                self.trainer_1.team.team.add(pokemon1_ListItem)
                self.dead_pokemon_2.add(pokemon2_ListItem)     #pokemon 2 added to dead queue
            #If the attacker (pokemon 2) is still alive and the defender (pokemon 1) is dead, then attacker (pokemon 2) lvls up and returns to back of queue.

            #Check for Fainting

            #If the attacker (pokemon 1) is still alive and the defender (pokemon 2) is dead, then attacker (pokemon 1) lvls up and returns to back of queue.
            if pokemon1.is_alive() and not pokemon2.is_alive():
                pokemon1.level_up()
                self.trainer_1.team.team.add(pokemon1_ListItem)  #adds pokemon1 to sorted team
                self.dead_pokemon_2.add(pokemon2_ListItem)     #pokemon 2 added to dead team.
            #If the attacker (pokemon 2) is still alive and the defender (pokemon 1) is dead, then attacker (pokemon 2) lvls up and returns to back of queue.
            elif pokemon2.is_alive() and not pokemon1.is_alive():
                pokemon2.level_up()
                self.trainer_2.team.team.add(pokemon2_ListItem)
                self.dead_pokemon_1.add(pokemon1_ListItem)     #Pokemon 1 added to dead queue
            #If both pokemon1 and pokemon2 are alive after the battle phase, then both take 1 damage.
            else:
                pokemon1.defend(1) #pokemon1.health -=1
                pokemon2.defend(1) #pokemon2.health -=1

                #Covers the cases after they both take 1 damage.
                if pokemon1.is_alive() and pokemon2.is_alive():
                    self.trainer_1.team.team.add(pokemon1_ListItem)  #adds the pokemon back in to sorted team
                    self.trainer_2.team.team.add(pokemon2_ListItem)  #adds the pokemon back in to sorted team
                elif pokemon1.is_alive() and not pokemon2.is_alive():
                    self.trainer_1.team.team.add(pokemon1_ListItem)  # adds the pokemon back in to sorted team
                    self.dead_pokemon_2.add(pokemon2_ListItem)   # adds the pokemon into dead list.
                elif pokemon2.is_alive() and not pokemon1.is_alive():
                    self.trainer_2.team.team.add(pokemon2_ListItem)  # adds the pokemon back into sorted team
                    self.dead_pokemon_1.add(pokemon1_ListItem)       # adds the pokemon back into dead list
                else:
                    self.dead_pokemon_1.add(pokemon1_ListItem)  # adds the pokemon back into dead list
                    self.dead_pokemon_2.add(pokemon2_ListItem)   # adds the pokemon back into dead list
        print("team 1 after battle")
        self.trainer_1.get_team().team.print_items()
        print("team 2 after battle")
        self.trainer_2.get_team().team.print_items()



            # Determine the winner
        if self.trainer_1.team.team.is_empty():
            return self.trainer_2.team.team # returns the winning team, team 2
        elif self.trainer_2.team.team.is_empty():
            return self.trainer_1   # returns the winning team, team 1
        else:
            return None # returns None if draw.



'''
if __name__ == '__main__':
    t1 = Trainer('Ash')
    t2 = Trainer('Gary')
    b = Battle(t1, t2, BattleMode.OPTIMISE)
    b._create_teams()
    winner = b.commence_battle()

    if winner is None:
        print("Its a draw")
    else:
        print(f"The winner is {winner.get_name()}")

'''


t1 = Trainer('Ash')
t2 = Trainer('Gary')
b = Battle(t1, t2, BattleMode.SET)
b._create_teams()
print(t1.get_team())
print(t2.get_team())
b.commence_battle()
print(t1.get_team())
print(t2.get_team())