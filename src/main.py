import random
from Human_Player import HumanPlayer
from AI_Player import *

from Cell import Cell
from Game import Game
from UI import *

if __name__ == "__main__":
    # seed = "MGMT1317"
    seed = "1234"
    random.seed(seed)

    # 创建一些示例玩家
    players = [
        # HumanPlayer(1, 'Alice'),
        RandomPlayer(1, 'Alice'),
        RandomPlayer(2, 'Bob'),
    ]

    # 创建一些示例格子
    cells = [
        Cell((0, 0), 'Cell (0, 0)', 'start', None),
        Cell((0, 1), 'Cell (0, 1)', 'building', {'price': 100, 'rent': 20}),
        Cell((0, 2), 'Cell (0, 2)', 'building', {'price': 100, 'rent': 20}),
        Cell((0, 3), 'Cell (0, 3)', 'community_chest', {'reward': 100}),
        Cell((0, 4), 'Cell (0, 4)', 'building', {'price': 100, 'rent': 20}),
        Cell((0, 5), 'Cell (0, 5)', 'building', {'price': 100, 'rent': 20}),
        Cell((1, 0), 'Cell (1, 0)', 'go_to_jail', {'target_position': (5, 5)}),
        Cell((1, 5), 'Cell (1, 5)', 'building', {'price': 100, 'rent': 20}),
        Cell((2, 0), 'Cell (2, 0)', 'building', {'price': 100, 'rent': 20}),
        Cell((2, 5), 'Cell (2, 5)', 'chance', None),
        Cell((3, 0), 'Cell (3, 0)', 'building', {'price': 100, 'rent': 20}),
        Cell((3, 5), 'Cell (3, 5)', 'building', {'price': 100, 'rent': 20}),
        Cell((4, 0), 'Cell (4, 0)', 'community_chest', {'reward': 200}),
        Cell((4, 5), 'Cell (4, 5)', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 0), 'Cell (5, 0)', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 1), 'Cell (5, 1)', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 2), 'Cell (5, 2)', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 3), 'Cell (5, 3)', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 4), 'Cell (5, 4)', 'building', {'price': 100, 'rent': 20}),
        Cell((5, 5), 'Cell (5, 5)', 'jail', {'stayTerms': 2}),
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

    app = QApplication(sys.argv)
    main_window = UI(game)
    main_window.show()
    main_window.run()
    sys.exit(app.exec_())
