from collections import Counter
import math
import os
import random
import json

import numpy as np
from Action import Action
from Config import Config
from Player import Player

from copy import deepcopy
from math import exp


class RandomPlayer(Player):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.is_human = False

    def get_action(self, gameState, UI=None):
        action_list = gameState.get_action_list()
        match action_list:
            case []:
                assert False, "No action available"
            case [action]:
                return action
            case _:
                return random.choice(action_list)


class BaseAIPlayer(Player):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.is_human = False

    @staticmethod
    def exp_alive_round(player_num, cell_num, your_building_rent, other_building_rent, current_balance):
        output_per_round = Config.round_reduce + sum(other_building_rent) / \
            cell_num - sum(your_building_rent) / cell_num * (player_num - 1)
        return current_balance / output_per_round if output_per_round > 0 else Config.inf

    @staticmethod
    def exp_num_once(cell_num):
        return cell_num

    @staticmethod
    def exp_CDF(round, lambda_):
        return 1 - exp(-lambda_ * round)

    def get_action(self, gameState, UI=None):
        action_list = gameState.get_action_list()
        match action_list:
            case []:
                assert False, "No action available"
            case [action]:
                return action
            case _:
                action_type_list = [action.action_type for action in action_list]

                player_num = len(gameState.players)
                cell_num = len(gameState.cells)
                building_cell = [cell for cell in gameState.cells.values() if cell.type == 'building']
                balance = self.balance

                your_building_rent = [cell.rent for cell in building_cell if cell.owner == self.id]
                other_building_rent = [cell.rent for cell in building_cell if cell.owner !=
                                       self.id and cell.owner is not None]

                round = BaseAIPlayer.exp_alive_round(
                    player_num, cell_num, your_building_rent, other_building_rent, balance)
                exp_num = BaseAIPlayer.exp_num_once(cell_num)

                current_cell = gameState.cells[self.position]
                can_sell_rate = BaseAIPlayer.exp_CDF(round, exp_num)

                if 'buy' in action_type_list:
                    if (1 - Config.selling_rate * can_sell_rate) * current_cell.price < round * current_cell.rent / cell_num * (player_num - 1):
                        return action_list[action_type_list.index('buy')]
                    else:
                        return action_list[action_type_list.index('none')]
                elif 'sell' in action_type_list:
                    if Config.selling_rate * current_cell.price > round * current_cell.rent / cell_num * (player_num - 1):
                        return action_list[action_type_list.index('sell')]
                    else:
                        return action_list[action_type_list.index('none')]

                assert False, "No action available"


class SimplifiedState:
    @staticmethod
    def normalize(vec: dict):
        total = sum(vec.values())
        for k in vec.keys():
            vec[k] /= total
        return vec

    def __init__(self, player1, player2, player1_building_num, player2_building_num):
        self.players = {player1.id: deepcopy(player1), player2.id: deepcopy(player2)}
        for player in self.players.values():
            player.balance_float = player.balance
            player.in_jail_float = player.in_jail

        self.player1_building_float = player1_building_num
        self.player1_building_num = player1_building_num
        self.player2_building_float = player2_building_num
        self.player2_building_num = player2_building_num
        self.empty_building_num = Config.total_buildings - player1_building_num - player2_building_num
        self.weight = 1

    def to_string(self):
        p1 = self.players[1]
        p2 = self.players[2]
        return f"{p1.balance_state}|{p1.in_jail}|{p1.alive}|{p2.balance_state}|{p2.in_jail}|{p2.alive}|{self.player1_building_num}|{self.player2_building_num}|{self.empty_building_num}"

    def update_balance_state(self):
        player1, player2 = self.players.values()
        if player1.balance < Config.safe_balance or player2.balance < Config.safe_balance:
            if abs(player1.balance - player2.balance) < Config.risky_balance_diff and player1.balance / max(player2.balance, 0.01) >= 0.75 and player1.balance / max(player2.balance, 0.01) <= 1.33 or player1.balance == player2.balance:
                player1.balance_state = 'risky~'
                player2.balance_state = 'risky~'
            else:
                player1.balance_state = 'risky>' if player1.balance > player2.balance else 'risky<'
                player2.balance_state = 'risky>' if player2.balance > player1.balance else 'risky<'
        if player1.balance >= Config.safe_balance:
            player1.balance_state = 'safe'
        if player2.balance >= Config.safe_balance:
            player2.balance_state = 'safe'

    def get_action_type_dict(self, playerid):
        available_actions = {}
        if self.players[playerid].in_jail > 0:
            available_actions['in_jail'] = 1.0
        else:
            available_actions['none'] = Config.total_none
            available_actions['go_to_jail'] = Config.total_go_to_jail
            if playerid == 1:
                if self.player1_building_num > 0:
                    available_actions['sell'] = self.player1_building_num
                if self.player2_building_num > 0:
                    available_actions['pay_rent'] = self.player2_building_num
                if self.empty_building_num > 0:
                    available_actions['buy'] = self.empty_building_num
            elif playerid == 2:
                if self.player1_building_num > 0:
                    available_actions['pay_rent'] = self.player1_building_num
                if self.player2_building_num > 0:
                    available_actions['sell'] = self.player2_building_num
                if self.empty_building_num > 0:
                    available_actions['buy'] = self.empty_building_num
            else:
                assert False, "Only support 2 players"
        # Normalize
        return SimplifiedState.normalize(available_actions)

    def get_next_state(self, action):
        next_gameState = deepcopy(self)
        player = next_gameState.players[action.player_id]
        another_player = next_gameState.players[3 - action.player_id]

        if action.player_id == 1:
            match action.action_type:
                case 'none':
                    pass
                case 'buy':
                    player.balance -= Config.building_price
                    next_gameState.player1_building_num += 1
                    next_gameState.empty_building_num -= 1
                case 'sell':
                    player.balance += Config.building_price * Config.selling_rate
                    next_gameState.player1_building_num -= 1
                    next_gameState.empty_building_num += 1
                case 'pay_rent':
                    player.balance -= Config.building_rent
                    another_player.balance += Config.building_rent
                case 'in_jail':
                    player.in_jail -= 1
                case 'go_to_jail':
                    player.in_jail = Config.jail_terms
                case 'get_reward':
                    player.balance += Config.rewards
                case _:
                    assert False, "Invalid action"
        elif action.player_id == 2:
            match action.action_type:
                case 'none':
                    pass
                case 'buy':
                    player.balance -= Config.building_price
                    next_gameState.player2_building_num += 1
                    next_gameState.empty_building_num -= 1
                case 'sell':
                    player.balance += Config.building_price * Config.selling_rate
                    next_gameState.player2_building_num -= 1
                    next_gameState.empty_building_num += 1
                case 'pay_rent':
                    player.balance -= Config.building_rent
                    another_player.balance += Config.building_rent
                case 'in_jail':
                    player.in_jail -= 1
                case 'go_to_jail':
                    player.in_jail = Config.jail_terms
                case 'get_reward':
                    player.balance += Config.rewards
                case _:
                    assert False, "Invalid action"
        else:
            assert False, "Only support 2 players"

        next_gameState.update_balance_state()
        return next_gameState

    def combine(self, other, playerid, weight=1.0):
        for player, other_player in zip(self.players.values(), other.players.values()):
            if player.id == playerid:
                player.balance_float = round((player.balance_float * self.weight +
                                             other_player.balance_float * weight)/(self.weight + weight))
                player.balance = round(player.balance_float)
                player.in_jail_float = round((player.in_jail_float * self.weight +
                                             other_player.in_jail_float * weight)/(self.weight + weight))
                player.in_jail = round(player.in_jail_float)
                player.alive = player.alive and other_player.alive

        if playerid == 1:
            self.player1_building_float = (self.player1_building_float * self.weight +
                                           other.player1_building_float * weight)/(self.weight + weight)
            self.player1_building_num = round(self.player1_building_float)
        elif playerid == 2:
            self.player2_building_float = (self.player2_building_float * self.weight +
                                           other.player2_building_float * weight)/(self.weight + weight)
            self.player2_building_num = round(self.player2_building_float)
        else:
            assert False, "Only support 2 players"
        self.empty_building_num = Config.total_buildings - self.player1_building_num - self.player2_building_num

        self.weight += weight

        return self


class ValueIterationPlayer(Player):
    # 如果Config.VI_data_filepath存在，则从该文件中读取字典state2value，否则初始化state2value
    state2value = {}
    if os.path.exists(Config.VI_data_filepath):
        with open(Config.VI_data_filepath, 'r', encoding='utf-8') as f:
            state2value = json.load(f)
            # 将所有value为dict类型的value中的key变为int类型
            for key, value in state2value.items():
                if key != 'iter':
                    state2value[key] = {int(k): v for k, v in value.items()}

    @staticmethod
    def gamestate2state_str(gameState) -> SimplifiedState:
        assert len(gameState.players) == 2, "Only support 2 players"

        players = deepcopy(list(gameState.players.values()))
        cells = gameState.cells.values()
        total_buildings = [cell for cell in cells if cell.type == 'building']
        player1_building_num = len([building for building in total_buildings if building.owner == 1])
        player2_building_num = len([building for building in total_buildings if building.owner == 2])
        state = SimplifiedState(*players, player1_building_num, player2_building_num)
        state.update_balance_state()
        return state.to_string()

    @staticmethod
    def get_reward(action):
        reward = 0
        match action.action_type:
            case 'none':
                reward += 0
            case 'buy':
                reward -= Config.building_price
            case 'sell':
                reward += Config.building_price * Config.selling_rate
            case 'pay_rent':
                reward -= 2*Config.building_rent
            case 'in_jail':
                reward += 0
            case 'go_to_jail':
                reward += 0
            case 'get_reward':
                reward += Config.rewards
            case _:
                assert False, "Invalid action"
        return reward

    @staticmethod
    def update_value(state, player_id, state2value, gamma, simulate_num=100000):
        another_player_id = 3 - player_id
        if not state.players[player_id].alive and not state.players[another_player_id].alive:
            return 0
        if not state.players[player_id].alive:
            return -Config.inf
        if not state.players[another_player_id].alive:
            return Config.inf
        action_type_dict = state.get_action_type_dict(player_id)
        # 根据action_type_dict.values()为概率随机抽取对应的key
        can_buy = state.empty_building_num > 0
        can_sell = state.player1_building_num > 0 if player_id == 1 else state.player2_building_num > 0

        new_value = 0.0
        action_none = Action('none', player_id)
        for selected_action, prob in action_type_dict.items():
            action_list = []

            if selected_action == 'buy' and can_buy:
                action_list = [action_none, Action(selected_action, player_id)]
            elif selected_action == 'sell' and can_sell:
                action_list = [action_none, Action(selected_action, player_id)]
            elif selected_action not in ['buy', 'sell']:
                action_list = [Action(selected_action, player_id)]
            else:
                action_list = [action_none]

            next_states = [state.get_next_state(action) for action in action_list]
            next_state_strs = [next_state.to_string() for next_state in next_states]
            new_values = [ValueIterationPlayer.get_reward(
                a) + gamma * state2value[next_state_str][player_id] for a, next_state_str in zip(action_list, next_state_strs)]
            max_index = np.argmax(new_values)

            next_state = next_states[max_index]
            next_state_str = next_state_strs[max_index]

            state2value[next_state_str][-1] = state2value[next_state_str][-1] \
                .combine(next_state, player_id, prob*simulate_num)

            new_value += new_values[max_index] * prob
        return new_value

    @staticmethod
    def update_values(state2value, max_iter=Config.VI_max_iter, gamma=Config.VI_gamma, epislon=Config.VI_epislon):
        total_building_num = sum([config[2] == 'building' for config in Config.cell_config])

        players = {player[1]: Player(player[1], player[2]) for player in Config.players_config}
        for player1_balance_state in Config.all_balance_states:
            for player2_balance_state in Config.all_balance_states:
                if player1_balance_state.startswith('risky>') and player2_balance_state.startswith('risky>') or \
                        player1_balance_state.startswith('risky<') and player2_balance_state.startswith('risky<'):
                    continue
                for player1_in_jail in range(3):
                    for player2_in_jail in range(3):
                        for player1_alive in [True, False]:
                            for player2_alive in [True, False]:
                                for player1_building_num in range(total_building_num + 1):
                                    for player2_building_num in range(total_building_num - player1_building_num + 1):
                                        players[1].balance_state = player1_balance_state
                                        players[1].in_jail = player1_in_jail
                                        players[1].alive = player1_alive
                                        players[2].balance_state = player2_balance_state
                                        players[2].in_jail = player2_in_jail
                                        players[2].alive = player2_alive

                                        state = SimplifiedState(players[1], players[2],
                                                                player1_building_num, player2_building_num)
                                        state2value[state.to_string()][-1] = state

        for _ in range(max_iter):
            delta = 0
            for state_str, dictionary in state2value.items():
                if state_str == 'iter':
                    continue
                state = dictionary[-1]
                for player_id in state2value[state_str]:
                    if player_id == -1:
                        continue
                    value = state2value[state_str][player_id]
                    state2value[state_str][player_id] = ValueIterationPlayer.update_value(
                        state, player_id, state2value, gamma)
                    if delta < abs(value - state2value[state_str][player_id]):
                        max_delta_state_str = state_str
                    delta = max(delta, abs(value - state2value[state_str][player_id]))
            state2value['iter'] += 1
            if delta < epislon:
                ValueIterationPlayer.save_data(state2value)
                break
            print(f"iter {state2value['iter']} finished")
            print(f"delta: {delta}")
            dic = {k: v for k, v in state2value[max_delta_state_str].items() if k != -1}
            print(f"{max_delta_state_str}: {dic}")

            if state2value['iter'] % Config.VI_data_save_iter == 0:
                ValueIterationPlayer.save_data(state2value)

        return state2value

    # 保存state2value到./data/state2value.json中
    @staticmethod
    def save_data(state2value):
        with open(Config.VI_data_filepath, 'w', encoding='utf-8') as f:
            # 不保存state2value中value的key为-1的项
            result = {}
            for state_str, dictionary in state2value.items():
                if state_str != 'iter':
                    dictionary = {k: v for k, v in dictionary.items() if k != -1}
                result[state_str] = dictionary
            json.dump(result, f, ensure_ascii=False)

    @staticmethod
    def init_values():
        state2value = {}
        total_building_num = sum([config[2] == 'building' for config in Config.cell_config])

        players = {player[1]: Player(player[1], player[2]) for player in Config.players_config}
        for player1_balance_state in Config.all_balance_states:
            for player2_balance_state in Config.all_balance_states:
                if player1_balance_state.startswith('risky>') and player2_balance_state.startswith('risky>') or \
                        player1_balance_state.startswith('risky<') and player2_balance_state.startswith('risky<'):
                    continue
                for player1_in_jail in range(3):
                    for player2_in_jail in range(3):
                        for player1_alive in [True, False]:
                            for player2_alive in [True, False]:
                                for player1_building_num in range(total_building_num + 1):
                                    for player2_building_num in range(total_building_num - player1_building_num + 1):
                                        players[1].balance_state = player1_balance_state
                                        players[1].in_jail = player1_in_jail
                                        players[1].alive = player1_alive
                                        players[2].balance_state = player2_balance_state
                                        players[2].in_jail = player2_in_jail
                                        players[2].alive = player2_alive

                                        state = SimplifiedState(players[1], players[2],
                                                                player1_building_num, player2_building_num)
                                        state2value['iter'] = 0
                                        potential_value1 = Config.balance_states_potential[Config.all_balance_states.index(
                                            player1_balance_state)]
                                        potential_value2 = Config.balance_states_potential[Config.all_balance_states.index(
                                            player2_balance_state)]
                                        state2value[state.to_string()] = {
                                            1: potential_value1 + player1_building_num * Config.building_price + Config.start_balance, 2: potential_value2 + player2_building_num * Config.building_price + Config.start_balance}
        ValueIterationPlayer.update_values(state2value)

    def __init__(self, id, name, train=False):
        super().__init__(id, name)
        # self.balance -= 500
        self.is_human = False
        if ValueIterationPlayer.state2value == None or len(ValueIterationPlayer.state2value) == 0:
            if train:
                ValueIterationPlayer.state2value = ValueIterationPlayer.init_values()
            else:
                raise Exception("Please Iterate the Value first")
        elif train:
            ValueIterationPlayer.state2value = ValueIterationPlayer.update_values(ValueIterationPlayer.state2value)
        if Config.DEBUG:
            for state_str, dictionary in self.state2value.items():
                # 排除键为-1的项
                filtered_dictionary = {k: v for k, v in dictionary.items() if k != -1}
                print(f"{state_str}\t{filtered_dictionary}")

    def get_action(self, gameState, UI=None):
        action_list = gameState.get_action_list()
        match action_list:
            case []:
                assert False, "No action available"
            case [action]:
                return action
            case _:
                next_gamestates = [gameState.get_next_state(action) for action in action_list]
                next_states_str = [ValueIterationPlayer.gamestate2state_str(
                    next_gamestate) for next_gamestate in next_gamestates]
                try:
                    another_id = 3 - self.id
                    next_states_values = [ValueIterationPlayer.state2value[next_state_str][self.id] - ValueIterationPlayer.state2value[next_state_str][another_id] + ValueIterationPlayer.get_reward(action)
                                          for next_state_str, action in zip(next_states_str, action_list)]
                except:
                    print(f"non-exist state_str: {next_states_str}")
                # 返回next_states_values + get_reward(action)中最大的那个
                return action_list[next_states_values.index(max(next_states_values))]


class ExpMaxPlayer(Player):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.is_human = False

    @staticmethod
    def v1(gameState):
        # TODO
        pass

    def get_action(self, gameState, UI=None):
        action_list = gameState.get_action_list()
        match action_list:
            case []:
                assert False, "No action available"
            case [action]:
                return action
            case _:
                pass
