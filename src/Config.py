import os


class Config:
    DEBUG = False

    seed = "MGMT1317"
    start_balance = 5000
    round_reduce = 20
    selling_rate = 0.5

    all_balance_states = ['safe', 'risky<', 'risky~', 'risky>']
    safe_balance = 1000
    risky_balance_diff = 200
    all_directions = [1, -1]
    direction_enable = False

    belief_gamma = 0.9
    VI_max_iter = 1000
    VI_gamma = 0.99
    VI_epislon = 1e-4
    VI_data_save_iter = 10
    VI_data_filepath = os.path.join(os.path.dirname(__file__), '../data/VI_data.json')

    inf = 9999999

    # players_config = [['HumanPlayer', 1, 'Alice'], ['RandomPlayer', 2, 'Bob']]
    # players_config = [['RandomPlayer', 1, 'Alice'], ['RandomPlayer', 2, 'Bob']]
    # players_config = [['BaseAIPlayer', 1, 'Alice'], ['RandomPlayer', 2, 'Bob']]
    # players_config = [['ValueIterationPlayer', 1, 'Alice', True], ['RandomPlayer', 2, 'Bob']]
    players_config = [['ValueIterationPlayer', 1, 'Alice', True], ['BaseAIPlayer', 2, 'Bob']]

    cell_config = [[(0, 0), 'start', 'start', None],
                   [(0, 1), 'Building', 'building', {'price': 100, 'rent': 20}],
                   [(0, 2), 'Building', 'building', {'price': 100, 'rent': 20}],
                   [(0, 3), 'Reward', 'community_chest', {'reward': 100}],
                   [(0, 4), 'Building', 'building', {'price': 100, 'rent': 20}],
                   [(0, 5), 'Building', 'building', {'price': 100, 'rent': 20}],
                   [(1, 0), 'Go to jail', 'go_to_jail', {'target_position': (5, 5)}],
                   [(1, 5), 'Building', 'building', {'price': 100, 'rent': 20}],
                   [(2, 0), 'Building', 'building', {'price': 100, 'rent': 20}],
                   [(2, 5), 'Chance', 'chance', None],
                   [(3, 0), 'Building', 'building', {'price': 100, 'rent': 20}],
                   [(3, 5), 'Building', 'building', {'price': 100, 'rent': 20}],
                   [(4, 0), 'Reward', 'community_chest', {'reward': 100}],
                   [(4, 5), 'Building', 'building', {'price': 100, 'rent': 20}],
                   [(5, 0), 'Building', 'building', {'price': 100, 'rent': 20}],
                   [(5, 1), 'Building', 'building', {'price': 100, 'rent': 20}],
                   [(5, 2), 'Building', 'building', {'price': 100, 'rent': 20}],
                   [(5, 3), 'Building', 'building', {'price': 100, 'rent': 20}],
                   [(5, 4), 'Building', 'building', {'price': 100, 'rent': 20}],
                   [(5, 5), 'Jail', 'jail', {'stayTerms': 2}]]

    cell_connections = {
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

    total_cells = len(cell_config)
    total_none = sum([cell[2] == 'start' or cell[2] == 'chance' for cell in cell_config])
    total_go_to_jail = sum([cell[2] == 'go_to_jail' for cell in cell_config])
    total_jail = sum([cell[2] == 'jail' for cell in cell_config])
    total_buildings = sum([cell[2] == 'building' for cell in cell_config])
    total_reward_cells = sum([cell[2] == 'community_chest' for cell in cell_config])

    rewards = 100
    building_price = 100
    building_rent = 20
    jail_terms = 2
