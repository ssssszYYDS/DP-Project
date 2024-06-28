# How to run the code
To run this project, you just need to run the src/main.py script.

# UI(for Human Player)
src/main.py provides a functin `run_game`.

You may need to change the parameters in the src/Config.py to change different parameters in the game. e.g. `players_config = [['HumanPlayer', 1, 'Alice'], ['RandomPlayer', 2, 'Bob']]`

Then you need to initialize the game and run `run_game(game)`.

# UI(for AI Player)
src/main.py provides a functin `run_UI`.

You may need to change the parameters in the src/Config.py to change different parameters in the game. e.g. `players_config = [['ValueIterationPlayer', 1, 'Alice', False], ['BaseAIPlayer', 2, 'Bob']]`

Then you need to initialize the game and run `run_UI(game, step_time=0.05)`, where `step_time` is the time stop after each round in order to see the UI clearly.

# Evaluation

src/main.py provides a functin `evaluate`. This function will print the different winning rates for different players.

You can change the different evaluation players by yourself. Remember that `ValueIterationPlayer` needs the fourth parameter `train` which means that it will train the values first or not. We have already trained the values in the file data/VI_data.json.


# Config
This section details the configuration settings used for the Monopoly game simulation.

## General Settings

- `DEBUG`: Boolean flag for debug mode. Default is `False`.
- `seed`: The seed for random number generation. Default is `"MGMT1317"`.
- `start_balance`: The initial balance for each player. Default is `5000`.
- `round_reduce`: The number of rounds after which the game reduces certain parameters. Default is `20`.
- `selling_rate`: The rate at which properties can be sold. Default is `0.5`.

## Player Configuration

- `players_config`: List of players participating in the game. Each player is defined by their type, ID, name, and optional parameters. The current configuration is: `players_config = [['ValueIterationPlayer', 1, 'Alice', False], ['BaseAIPlayer', 2, 'Bob']]`

## Game Economics

- `inf`: Infinity value used for certain calculations. Default is `9999`.
- `rewards`: The reward amount for community chest cells. Default is `100`.
- `building_price`: The price of purchasing a building. Default is `100`.
- `building_rent`: The rent charged for landing on a purchased building. Default is `20`.
- `jail_terms`: The number of terms (turns) a player must stay in jail. Default is `2`.

