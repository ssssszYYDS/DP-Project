import random
from Human_Player import HumanPlayer
from AI_Player import *

from Cell import Cell
from Game import Game
from UI import *


def run_UI(game: Game):
    app = QApplication(sys.argv)
    main_window = UI(game)
    main_window.show()
    main_window.run(max_rounds=10000)
    sys.exit(app.exec_())


def run_game(game: Game):
    winner = game.run(max_rounds=10000)
    print(f"游戏结束！{winner.name}获胜！用时{game.game_state.round}轮")
    sys.exit()


if __name__ == "__main__":
    seed = "MGMT1317"
    random.seed(seed)

    # 创建一些示例玩家
    players = [
        # HumanPlayer(1, 'Alice'),
        RandomPlayer(1, 'Alice'),
        RandomPlayer(2, 'Bob'),
    ]

    # 创建一些示例格子
    cells = [
        Cell((0, 0), 'start', 'start', None),
        Cell((0, 1), 'Building', 'building', {'price': 100, 'rent': 20}),
        Cell((0, 2), 'Building', 'building', {'price': 100, 'rent': 20}),
        Cell((0, 3), 'Cell (0, 3)', 'community_chest', {'reward': 100}),
        Cell((0, 4), 'Building', 'building', {'price': 100, 'rent': 20}),
        Cell((0, 5), 'Building', 'building', {'price': 100, 'rent': 20}),
        Cell((1, 0), 'Go to jail', 'go_to_jail', {'target_position': (5, 5)}),
        Cell((1, 5), 'Building', 'building', {'price': 100, 'rent': 20}),
        Cell((2, 0), 'Building', 'building', {'price': 100, 'rent': 20}),
        Cell((2, 5), 'Chance', 'chance', None),
        Cell((3, 0), 'Building', 'building', {'price': 100, 'rent': 20}),
        Cell((3, 5), 'Building', 'building', {'price': 100, 'rent': 20}),
        Cell((4, 0), 'Reward', 'community_chest', {'reward': 200}),
        Cell((4, 5), 'Building', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 0), 'Building', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 1), 'Building', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 2), 'Building', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 3), 'Building', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 4), 'Building', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 5), 'Jail', 'jail', {'stayTerms': 2}),
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
        (5, 1): {1: (5, 0), -1: (5, 2)},
        (5, 2): {1: (5, 1), -1: (5, 3)},
        (5, 3): {1: (5, 2), -1: (5, 4)},
        (5, 4): {1: (5, 3), -1: (5, 5)},
        (5, 5): {1: (5, 4), -1: (4, 5)},
    }

    # 初始化游戏状态
    game = Game(players, cells, connections)

    run_UI(game)
    # run_game(game)
