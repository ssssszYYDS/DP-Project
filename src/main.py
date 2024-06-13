import random
from Human_Player import HumanPlayer
from AI_Player import *

from Cell import Cell
from Game import Game
from UI import *


from Config import Config


def run_UI(game: Game, *args, **kwargs):
    app = QApplication(sys.argv)
    main_window = UI(game)
    main_window.show()
    main_window.run(max_rounds=10000, *args, **kwargs)
    app.exec_()


def run_game(game: Game):
    winner = game.run(max_rounds=10000)
    print(f"游戏结束！{winner.name}获胜！用时{game.game_state.round}轮")
    return winner.name, game.game_state.round


def get_win_rate(game_times: int = 100):
    win_count = {player[2]: 0 for player in Config.players_config}
    total_round = {player[2]: 0 for player in Config.players_config}
    for _ in range(game_times):
        players = [eval(player[0])(player[1], player[2]) for player in Config.players_config]
        cells = [Cell(*args) for args in Config.cell_config]
        connections = Config.cell_connections
        game = Game(players, cells, connections)
        winner_name, round = run_game(game)
        win_count[winner_name] += 1
        total_round[winner_name] += round
    return {name: {'win_rate': win_count[name] / game_times, 'avg_round': total_round[name] / win_count[name] if win_count[name] > 0 else 0.0} for name in win_count}


if __name__ == "__main__":
    random.seed(Config.seed)

    players = [eval(player[0])(*player[1:]) for player in Config.players_config]
    cells = [Cell(*args) for args in Config.cell_config]
    connections = Config.cell_connections

    # 初始化游戏状态
    game = Game(players, cells, connections)

    # run_UI(game)
    # run_game(game)
    # print(get_win_rate(100))
    run_UI(game, step_time=0.05)
    # time.sleep(10)
