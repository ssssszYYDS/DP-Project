from Player import Player
from Action import Action
from UI import UI


class HumanPlayer(Player):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.is_human = True

    def get_action(self, gameState, UI=None):
        action_list = self.get_action_list(gameState)
        if UI is not None:
            return UI.get_action(action_list)
        match action_list:
            case []:
                print("No actions available")
                return Action('none', self.id)
            case [action]:
                return action
            case _:
                action_index = input(f"Enter the index of the action you want to perform: \n{action_list}")
                action = action_list[int(action_index)]
                return action
