from __future__ import annotations
from poke_team import Trainer, PokeTeam
from typing import Tuple
from battle_mode import BattleMode

class Battle:

    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion = "health") -> None:
        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2
        self.battle_mode = battle_mode
        self.criterion = criterion

    def commence_battle(self) -> Trainer | None:
        raise NotImplementedError

    def _create_teams(self) -> None:
        raise NotImplementedError

    # Note: These are here for your convenience
    # If you prefer you can ignore them

    #This function will use a stack as the last pokemon selected is the first pokemon battling.
    def set_battle(self) -> PokeTeam | None:
        raise NotImplementedError

    #This function will use a circular Queue implementation as the each pokemon is sent back to the end of the battle queue after
    #each pokemon battle.
    def rotate_battle(self) -> PokeTeam | None:
        while not self.trainer1.team.is_empty() and not self.trainer2.team.is_empty():
        # serve the first Pokémon of each team for the battle
            pokemon1 = self.trainer1.team.serve()
            pokemon2 = self.trainer2.team.serve()
            
            #Battle Logic
            #If P1 speed is greater than P2
            if pokemon1.get_speed() > pokemon2.get_speed():
                damage = pokemon1.attack(pokemon2)
                pokemon2.defend(damage)
                #If P2 speed is greater than P1
            elif pokemon1.get_speed() < pokemon2.get_speed():
                damage = pokemon2.attack()
                pokemon1.defend(damage)
            else:
                # Perform simultaneous attacks, if speed is same.
                damage_to_p2 = pokemon1.attack(pokemon2)
                damage_to_p1 = pokemon2.attack(pokemon1)
            pokemon1.defend(damage_to_p2)
            pokemon2.defend(damage_to_p1)
            # If both Pokémon are still alive, the defender counterattacks
            if pokemon1.is_alive() and pokemon2.is_alive():
                # Let's decide that pokemon1 was the initial attacker for simplicity,
                # and thus pokemon2 gets to counterattack
                counter_damage_to_p1 = pokemon2.attack(pokemon1)
                pokemon1.defend(counter_damage_to_p1)
    
    #In the optimised mode. User picks a stat to order their team.The initial order will be maintained even if a certain stat decreases.
    #The stats are stored in the criterion list in task 2.
    #The assign method in Task 2 assigns the order of the team based on the chosen attribute from the criterion list.
    #therefore i believe using a sorted list is the best method in order to do this task as you can sort the team based on the attribute.
    def optimise_battle(self) -> PokeTeam | None:
        raise NotImplementedError


if __name__ == '__main__':
    t1 = Trainer('Ash')
    t2 = Trainer('Gary')
    b = Battle(t1, t2, BattleMode.ROTATE)
    b._create_teams()
    winner = b.commence_battle()

    if winner is None:
        print("Its a draw")
    else:
        print(f"The winner is {winner.get_name()}")
