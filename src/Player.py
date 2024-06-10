from abc import abstractmethod
import random


class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.balance = 1500
        self.position = (-1, -1)
        self.direction = random.choice([1, -1])
        self.in_jail = 0
        self.cells_owned = []
        self.alive = True

        self.has_moved = False

    @abstractmethod
    def get_action(self, gameState, UI=None):
        pass

    def __repr__(self):
        return f"Player({self.id}, '{self.name}', {self.position}, {self.direction}, {self.balance}, {self.cells_owned})"

    def get_info(self):
        return f"玩家{self.id}: {self.name}, \t余额: {self.balance}, \t当前位置: {self.position}, \t监狱状态: {self.in_jail}, \t拥有地产数量: {len(self.cells_owned)}"
