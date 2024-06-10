import random


class Action:
    all_actions = ['none', 'move', 'buy', 'sell', 'pay_rent', 'in_jail', 'go_to_jail', 'get_reward']

    def __init__(self, action_type, player_id):
        self.action_type = action_type  # 动作类型，如'move', 'buy', 'sell', 'pay_rent'等
        self.player_id = player_id      # 执行动作的玩家ID

    def perform(self, gameState):
        # 基于动作类型对游戏状态进行更新
        match self.action_type:
            case 'none':
                pass
            case 'move':
                self.move_player(gameState)
            case 'buy':
                self.buy_property(gameState)
            case 'sell':
                self.sell_property(gameState)
            case 'pay_rent':
                self.pay_rent(gameState)
            case 'in_jail':
                self.in_jail(gameState)
            case 'go_to_jail':
                self.go_to_jail(gameState)
            case 'get_reward':
                self.get_reward(gameState)
            case _:
                raise ValueError("Invalid action type")

    def move_player(self, gameState):
        # 更新玩家位置的逻辑
        player = gameState.players[self.player_id]
        # 计算新位置
        step_number = random.randint(1, 6)
        print(f"Player {player.id} moves {step_number} steps")
        current_position = player.position
        for _ in range(step_number):
            current_position = gameState.cell_connections[current_position][player.direction]
            if current_position is None:
                raise ValueError("Invalid move")

        player.position = current_position
        player.has_moved = True

    def buy_property(self, gameState):
        # 购买地产的逻辑
        player = gameState.players[self.player_id]
        cell = gameState.cells[player.position]

        assert player.balance >= cell.price, "Player does not have enough balance to buy the property"

        player.balance -= cell.price
        player.cells_owned.append(cell)
        cell.owner = player.id

    def sell_property(self, gameState):
        # 卖出地产的逻辑
        player = gameState.players[self.player_id]
        cell = gameState.cells[player.position]

        assert cell in player.cells_owned, "Player does not own the property"

        player.balance += cell.price
        player.cells_owned.remove(cell)
        cell.owner = None

    def pay_rent(self, gameState):
        # 支付租金的逻辑
        player = gameState.players[self.player_id]
        cell = gameState.cells[player.position]
        owner = gameState.players[cell.owner]
        player.balance -= cell.rent
        owner.balance += cell.rent
        if player.balance < 0:
            player.alive = False

    def in_jail(self, gameState):
        # 玩家进入监狱的逻辑
        player = gameState.players[self.player_id]
        player.in_jail -= 1

    def go_to_jail(self, gameState):
        # 玩家进入监狱的逻辑
        player = gameState.players[self.player_id]
        player.position = gameState.cells[player.position].target_position
        player.in_jail = gameState.cells[player.position].stayTerms

    def get_reward(self, gameState):
        # 玩家进入监狱的逻辑
        player = gameState.players[self.player_id]
        player.balance += gameState.cells[player.position].reward

    def __repr__(self):
        return f"Action('{self.action_type}', {self.player_id})"
