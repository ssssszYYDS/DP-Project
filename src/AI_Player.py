import random
from Action import Action
from Player import Player


class RandomPlayer(Player):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.is_human = False

    def get_action(self, gameState):
        action_list = gameState.get_action_list()
        match action_list:
            case []:
                return Action('none', self.id)
            case [action]:
                return action
            case _:
                return random.choice(action_list)
