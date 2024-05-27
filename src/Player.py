from abc import abstractmethod
import random

from Action import Action


class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.position = (-1, -1)
        self.direction = random.choice([1, -1])
        self.balance = 1500
        self.in_jail = 0
        self.cells_owned = []
        self.alive = True

        self.has_moved = False

    @abstractmethod
    def get_action(self, gameState, UI=None):
        pass

    def get_action_list(self, gameState):
        action_list = []
        if self.in_jail > 0:
            # 在监狱中
            action_list.append(Action('in_jail', self.id))
        elif not self.has_moved:
            # 移动
            action_list.append(Action('move', self.id))
        else:
            current_cell = gameState.cells[self.position]
            match current_cell.type:
                case 'building':
                    match current_cell.owner:
                        case None:
                            action_list.append(Action('none', self.id))
                            action_list.append(Action('buy', self.id))
                        case self.id:
                            action_list.append(Action('none', self.id))
                            action_list.append(Action('sell', self.id))
                        case _:
                            action_list.append(Action('pay_rent', self.id))
                case 'go_to_jail':
                    action_list.append(Action('go_to_jail', self.id))
                case 'community_chest':
                    action_list.append(Action('get_reward', self.id))
                case _:
                    action_list.append(Action('none', self.id))
        return action_list

    def __repr__(self):
        return f"Player({self.id}, '{self.name}', {self.position}, {self.direction}, {self.balance}, {self.cells_owned})"
