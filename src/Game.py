import random
from time import sleep
from Human_Player import HumanPlayer
from AI_Player import RandomPlayer

from Action import Action
from copy import deepcopy

from Config import Config


class GameState:
    def __init__(self, players, cells, connections, current_player_id=1):
        self.current_player_id = current_player_id
        self.players = {player.id: player for player in players}
        self.cells = {cell.position: cell for cell in cells}
        self.cell_connections = connections

        self.round = 0

    def __repr__(self):
        return f"GameState: \n" \
            f"Current Player: {self.players[self.current_player_id].name}, \n" \
            f"Players: {self.players}, \n" \
            f"cells: {self.cells}\n"

    def get_action_list(self):
        player = self.players[self.current_player_id]

        action_list = []
        if player.in_jail > 0:
            # 在监狱中
            action_list.append(Action('in_jail', player.id))
        elif not player.has_moved:
            # 移动
            action_list.append(Action('move', player.id))
        else:
            current_cell = self.cells[player.position]
            match current_cell.type:
                case 'building':
                    match current_cell.owner:
                        case None:
                            action_list.append(Action('none', player.id))
                            if player.balance >= current_cell.price:
                                action_list.append(Action('buy', player.id))
                        case player.id:
                            action_list.append(Action('none', player.id))
                            action_list.append(Action('sell', player.id))
                        case _:
                            action_list.append(Action('pay_rent', player.id))
                case 'go_to_jail':
                    action_list.append(Action('go_to_jail', player.id))
                case 'community_chest':
                    action_list.append(Action('get_reward', player.id))
                case _:
                    action_list.append(Action('none', player.id))
        return action_list

    def get_next_state(self, action: Action):
        next_state = deepcopy(self)
        action.perform(next_state)
        return next_state


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
        return sum(player.alive for player in self.game_state.players.values()) <= 1

    def get_winner(self):
        # 返回获胜者
        return max(self.game_state.players.values(), key=lambda x: x.balance)

    def update_UI(self):
        if self.UI:
            self.UI.update_game_info_ui()
            self.UI.update_game_board_ui()

    def run(self, max_rounds: int = 10000, step_time: float = 0.0):
        # 主游戏循环
        while not self.is_finished():
            current_player = self.game_state.players[self.game_state.current_player_id]

            # 从当前玩家处获取动作2次(一次移动，一次其他动作)
            for _ in range(2):
                action = current_player.get_action(self.game_state, self.UI)
                if Config.DEBUG:
                    print(f"current player: {current_player.name}, \taction: {action.action_type}")

                # 更新游戏状态
                self.update_game_state(action)
                self.update_UI()

            # 切换到下一个玩家
            self.game_state.current_player_id += 1

            # 一轮结束
            if self.game_state.current_player_id > len(self.game_state.players):
                self.game_state.current_player_id = 1
                self.game_state.round += 1
                for player in self.game_state.players.values():
                    player.has_moved = False

                    player.balance -= Config.round_reduce  # 每一轮结束时扣除一定金额
                    if player.balance < 0:
                        player.alive = False

                self.update_UI()

            if self.game_state.round > max_rounds:
                break

            if step_time > 0:
                sleep(step_time)

        return self.get_winner()

    def reset(self):
        # 重置游戏状态
        self.score = 0
        self.game_state = deepcopy(self.init_game_state)

    def __repr__(self):
        return f"score: {self.score},\ngame_state:\n{self.game_state}"
