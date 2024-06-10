from abc import abstractmethod
import random


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

    def __repr__(self):
        return f"Player({self.id}, '{self.name}', {self.position}, {self.direction}, {self.balance}, {self.cells_owned})"
