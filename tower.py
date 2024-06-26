from poke_team import Trainer, PokeTeam
from enum import Enum
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from typing import Tuple

class BattleTower:
    MIN_LIVES = 1
    MAX_LIVES = 3
    def __init__(self) -> None:
        self.player_trainer = Trainer("Player trainer")
        

    # Hint: use random.randint() for randomisation
    def set_my_trainer(self, trainer: Trainer) -> None:
        raise NotImplementedError

    def generate_enemy_trainers(self, num_teams: int) -> None:
        raise NotImplementedError

    def battles_remaining(self) -> bool:
        raise NotImplementedError

    def next_battle(self) -> Tuple[Trainer, Trainer, Trainer, int, int]:
        raise NotImplementedError

    def enemies_defeated(self) -> int:
        raise NotImplementedError