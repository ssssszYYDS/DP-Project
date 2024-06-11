from abc import abstractmethod
import random

from Action import Action
from Config import Config


class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.balance = Config.start_balance
        self.position = (-1, -1)
        self.direction = random.choice(Config.all_directions) if Config.direction_enable else 1
        self.in_jail = 0
        self.cells_owned = []
        self.alive = True

        self.has_moved = False

        self.belief = {action_type: 0.01 for action_type in Action.all_actions}

    @abstractmethod
    def get_action(self, gameState, UI=None):

        pass

    def beta(a, b):
        return a / (a + b)

    def get_belief(self, gameState):
        action_list = gameState.get_action_list()
        match action_list:
            case []:
                assert False, "No action available"
            case [action]:
                return [1.0]
            case _:
                assert len(action_list) == 2, "Only support 2 actions"
                a = self.belief[action_list[0].action_type]
                b = self.belief[action_list[1].action_type]
                return [self.beta(a, b), self.beta(b, a)]

    def __repr__(self):
        return f"Player({self.id}, '{self.name}', {self.position}, {self.direction}, {self.balance}, {self.cells_owned})"

    def get_info(self):
        return f"玩家{self.id}: {self.name}, \t余额: {self.balance}, \t当前位置: {self.position}, \t监狱状态: {self.in_jail}, \t拥有地产数量: {len(self.cells_owned)}"
