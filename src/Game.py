import random
from Human_Player import HumanPlayer
from AI_Player import RandomPlayer

from Cell import Cell
from Action import Action
from copy import deepcopy


class GameState:
    def __init__(self, players, cells, connections, current_player_id=1):
        self.current_player_id = current_player_id
        self.players = {player.id: player for player in players}
        self.cells = {cell.position: cell for cell in cells}
        self.cell_connections = connections

    def __repr__(self):
        return f"GameState: \n" \
            f"Current Player: {self.players[self.current_player_id].name}, \n" \
            f"Players: {self.players}, \n" \
            f"cells: {self.cells}\n"


class Game:
    def __init__(self, players, cells, connections):
        self.UI = None
        self.score = 0
        self.cell_number = len(cells)

        self.game_state = GameState(players, cells, connections)

        if not self.check_valid_map():
            raise ValueError("Invalid map")

        for player in players:
            player.position = random.choice(list(self.game_state.cells.keys()))
        self.init_game_state = deepcopy(self)

    def check_valid_map(self):
        # 检查地图是否合法
        for cell in self.game_state.cells.values():
            if cell.position not in self.game_state.cell_connections:
                return False
            for direction in self.game_state.cell_connections[cell.position]:
                if self.game_state.cell_connections[cell.position][direction] not in self.game_state.cells:
                    return False
        return True

    def update_game_state(self, action: Action):
        # 根据动作更新游戏状态
        action.perform(self.game_state)

    def is_finished(self):
        # 判断游戏是否结束
        return not (self.game_state.players[1].alive and self.game_state.players[2].alive)

    def is_winner(self):
        # 返回获胜者
        return self.game_state.players[1].alive

    def main_UI(self):
        print(f"Game started with UI")
        # 主游戏循环
        while not self.is_finished():
            current_player = self.game_state.players[self.game_state.current_player_id]

            # 从当前玩家处获取动作
            if current_player.is_human:
                action = current_player.get_action(self.game_state, self.UI)
            else:
                action = current_player.get_action(self.game_state)
            print(f"current player: {current_player.name}, action: {action.action_type}")

            # 更新游戏状态
            self.update_game_state(action)
            self.UI.update_game_info_ui()
            self.UI.update_game_board_ui()

            # 切换到下一个玩家
            self.game_state.current_player_id += 1

            if self.game_state.current_player_id > len(self.game_state.players):
                self.game_state.current_player_id = 1
                for player in self.game_state.players.values():
                    player.has_moved = False

    def run(self):
        # 主游戏循环
        while not self.is_finished():
            current_player = self.game_state.players[self.game_state.current_player_id]

            # 从当前玩家处获取动作
            if self.UI is not None and current_player.is_human:
                action = current_player.get_action(self.game_state, self.UI)
            else:
                action = current_player.get_action(self.game_state)
            print(f"current player: {current_player.name}, action: {action.action_type}")

            # 更新游戏状态
            self.update_game_state(action)
            self.UI.update_game_info_ui()
            self.UI.update_game_board_ui()

            # 切换到下一个玩家
            self.game_state.current_player_id += 1

            if self.game_state.current_player_id > len(self.game_state.players):
                self.game_state.current_player_id = 1
                for player in self.game_state.players.values():
                    player.has_moved = False

    def reset(self):
        # 重置游戏状态
        self.score = 0
        self.game_state = deepcopy(self.init_game_state)

    def __repr__(self):
        return f"score: {self.score},\ngame_state:\n{self.game_state}"


if __name__ == "__main__":
    # 创建一些示例玩家
    players = [
        HumanPlayer(1, 'Alice'),
        RandomPlayer(2, 'Bob'),
    ]

    # 创建一些示例格子
    cells = [
        Cell((0, 0), 'Cell (0, 0)', 'building', {'price': 100, 'rent': 20}),
        Cell((0, 1), 'Cell (0, 1)', 'building', {'price': 100, 'rent': 20}),
        Cell((0, 2), 'Cell (0, 2)', 'building', {'price': 100, 'rent': 20}),
        Cell((0, 3), 'Cell (0, 3)', 'building', {'price': 100, 'rent': 20}),
        Cell((0, 4), 'Cell (0, 4)', 'building', {'price': 100, 'rent': 20}),
        Cell((0, 5), 'Cell (0, 5)', 'building', {'price': 100, 'rent': 20}),
        Cell((1, 0), 'Cell (1, 0)', 'building', {'price': 100, 'rent': 20}),
        Cell((1, 5), 'Cell (1, 5)', 'building', {'price': 100, 'rent': 20}),
        Cell((2, 0), 'Cell (2, 0)', 'building', {'price': 100, 'rent': 20}),
        Cell((2, 5), 'Cell (2, 5)', 'building', {'price': 100, 'rent': 20}),
        Cell((3, 0), 'Cell (3, 0)', 'building', {'price': 100, 'rent': 20}),
        Cell((3, 5), 'Cell (3, 5)', 'building', {'price': 100, 'rent': 20}),
        Cell((4, 0), 'Cell (4, 0)', 'building', {'price': 100, 'rent': 20}),
        Cell((4, 5), 'Cell (4, 5)', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 0), 'Cell (5, 0)', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 1), 'Cell (5, 1)', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 2), 'Cell (5, 2)', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 3), 'Cell (5, 3)', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 4), 'Cell (5, 4)', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 5), 'Cell (5, 5)', 'building', {'price': 100, 'rent': 20}),
    ]

    connections = {
        (0, 0): {1: (0, 1), -1: (1, 0)},
        (0, 1): {1: (0, 2), -1: (0, 0)},
        (0, 2): {1: (0, 3), -1: (0, 1)},
        (0, 3): {1: (0, 4), -1: (0, 2)},
        (0, 4): {1: (0, 5), -1: (0, 3)},
        (0, 5): {1: (1, 5), -1: (0, 4)},
        (1, 0): {1: (0, 0), -1: (2, 0)},
        (1, 5): {1: (2, 5), -1: (0, 5)},
        (2, 0): {1: (1, 0), -1: (3, 0)},
        (2, 5): {1: (3, 5), -1: (1, 5)},
        (3, 0): {1: (2, 0), -1: (4, 0)},
        (3, 5): {1: (4, 5), -1: (2, 5)},
        (4, 0): {1: (3, 0), -1: (5, 0)},
        (4, 5): {1: (5, 5), -1: (3, 5)},
        (5, 0): {1: (4, 0), -1: (5, 1)},
        (5, 1): {1: (5, 2), -1: (5, 0)},
        (5, 2): {1: (5, 3), -1: (5, 1)},
        (5, 3): {1: (5, 4), -1: (5, 2)},
        (5, 4): {1: (5, 5), -1: (5, 3)},
        (5, 5): {1: (4, 5), -1: (5, 4)},
    }

    # 初始化游戏状态
    initial_game = Game(players, cells, connections)

    # 显示初始游戏状态
    print(initial_game)
