import sys
import os
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, QDialog, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QGridLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from Action import Action
import time
from PyQt5.QtCore import QTimer


class UI(QMainWindow):
    def __init__(self, game):
        super().__init__()

        self.game = game
        self.game.UI = self

        self.last_action = None

        self.type2color = {
            'building': 'lightblue',
            'start': 'green',
            'jail': 'orange',
            'go_to_jail': 'red',
            'chance': 'yellow',
            'community_chest': 'purple',
        }
        self.playerid2color = {
            1: 'lightgreen',
            2: 'blue',
        }

        self.initUI()

    def initUI(self):
        self.setWindowTitle("大富翁游戏")
        self.setGeometry(100, 100, 1200, 1200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.create_game_info_ui()
        self.create_game_board_ui()
        self.update_game_info_ui()
        self.update_game_board_ui()

    def create_game_info_ui(self):
        # Create a layout for game info
        self.game_info_layout = QHBoxLayout()

        self.player_info = QLabel("玩家信息")
        self.game_info_layout.addWidget(self.player_info)

        self.layout.addLayout(self.game_info_layout)

    def create_game_board_ui(self):

        # 创建游戏棋盘
        self.board_widget = QWidget()
        self.board_layout = QGridLayout(self.board_widget)
        self.board_layout.setSpacing(2)

        self.cells_widgets = {}
        for position, cell in self.game.game_state.cells.items():
            cell_widget = QLabel()
            cell_widget.setAlignment(Qt.AlignCenter)
            # 根据单元格类型设置背景颜色
            cell_bg_color = self.type2color.get(cell.type, 'lightgrey')

            cell_widget.setStyleSheet(f"""
                QLabel {{
                    background-color: {cell_bg_color};
                    border: 1px solid black;
                }}
            """)

            self.board_layout.addWidget(cell_widget, position[0], position[1])
            self.cells_widgets[position] = cell_widget

        self.layout.addWidget(self.board_widget)

    def update_game_info_ui(self):
        # Update the player info
        player_info_text = "玩家信息:\n"
        for player_id, player in self.game.game_state.players.items():
            player_info_text += f"{player.get_info()}, \n"
        self.player_info.setText(player_info_text)

    def update_game_board_ui(self):
        for position, cell in self.game.game_state.cells.items():
            cell_widget = self.cells_widgets[position]
            text = cell.name

            cell_bg_color = self.type2color.get(cell.type, 'lightgrey')
            cell_widget.setStyleSheet(f"""
                QLabel {{
                    background-color: {cell_bg_color};
                    border: 1px solid black;
                }}
            """)

            # 为每个player的位置更新单元格显示
            for player_id, player in self.game.game_state.players.items():
                if player.position == position:
                    text += f"\n👦🏻{player.name}"

                if cell.type == 'building' and cell.owner == player_id:
                    cell_bg_color = self.playerid2color.get(player_id, 'grey')
                    cell_widget.setStyleSheet(f"""
                        QLabel {{
                            background-color: {cell_bg_color};
                            border: 1px solid black;
                        }}
                    """)

            cell_widget.setText(text)

    def none_operation(self):
        self.last_action = 'none'

    def move_player(self):
        self.last_action = 'move'

    def buy_property(self):
        self.last_action = 'buy'

    def sell_property(self):
        self.last_action = 'sell'

    def pay_rent(self):
        self.last_action = 'pay_rent'

    def in_jail(self):
        self.last_action = 'in_jail'

    def go_to_jail(self):
        self.last_action = 'go_to_jail'

    def get_reward(self):
        self.last_action = 'get_reward'

    def show_message(self, message: str):
        msg = QMessageBox()
        msg.setText(message)
        msg.exec_()

    def get_action(self, action_list: list[Action]):
        action_type_list = [action.action_type for action in action_list]

        dialog = QDialog(self)
        dialog.setWindowTitle("选择操作")
        dialog.setGeometry(1500, 300, 500, 500)
        dialog.setModal(True)

        layout = QVBoxLayout(dialog)

        button_box = QVBoxLayout()  # 修改为 QVBoxLayout

        # 创建一个 lambda 函数用来处理按钮点击事件
        def button_clicked(action_type):
            # 在这个函数内部创建 Action 并返回
            self.last_action = Action(action_type, self.game.game_state.current_player_id)
            dialog.accept()

        # 以下生成按钮的代码部分不变，只是将点击事件连接到新的 lambda 函数
        none_button = QPushButton("无操作")
        none_button.clicked.connect(lambda: button_clicked('none'))
        none_button.setEnabled('none' in action_type_list)
        button_box.addWidget(none_button)

        # 对于每个操作，重复上述步骤
        move_button = QPushButton("移动")
        move_button.clicked.connect(lambda: button_clicked('move'))
        move_button.setEnabled('move' in action_type_list)
        button_box.addWidget(move_button)

        buy_button = QPushButton("购买")
        buy_button.clicked.connect(lambda: button_clicked('buy'))
        buy_button.setEnabled('buy' in action_type_list)
        button_box.addWidget(buy_button)

        sell_button = QPushButton("出售")
        sell_button.clicked.connect(lambda: button_clicked('sell'))
        sell_button.setEnabled('sell' in action_type_list)
        button_box.addWidget(sell_button)

        pay_rent_button = QPushButton("支付租金")
        pay_rent_button.clicked.connect(lambda: button_clicked('pay_rent'))
        pay_rent_button.setEnabled('pay_rent' in action_type_list)
        button_box.addWidget(pay_rent_button)

        in_jail_button = QPushButton("进入监狱")
        in_jail_button.clicked.connect(lambda: button_clicked('in_jail'))
        in_jail_button.setEnabled('in_jail' in action_type_list)
        button_box.addWidget(in_jail_button)

        go_to_jail_button = QPushButton("前往监狱")
        go_to_jail_button.clicked.connect(lambda: button_clicked('go_to_jail'))
        go_to_jail_button.setEnabled('go_to_jail' in action_type_list)
        button_box.addWidget(go_to_jail_button)

        get_reward_button = QPushButton("领取奖励")
        get_reward_button.clicked.connect(lambda: button_clicked('get_reward'))
        get_reward_button.setEnabled('get_reward' in action_type_list)
        button_box.addWidget(get_reward_button)

        layout.addLayout(button_box)  # 将按钮布局加入主布局中

        if dialog.exec_() == QDialog.Accepted:
            return self.last_action

        return Action("none", self.game.game_state.current_player_id)  # 如果没有选择操作，返回 "none"

    def run(self, *args, **kwargs):
        winner = self.game.run(*args, **kwargs)
        self.show_message(f"游戏结束！{winner.name}获胜！用时{self.game.game_state.round}轮")
        sys.exit()

    def show_blocking_window(self, step_time):
        blocking_window = BlockingWindow(step_time, self)
        blocking_window.exec_()


class BlockingWindow(QDialog):
    def __init__(self, step_time, parent=None):
        super().__init__(parent)
        self.setWindowTitle("请等待")
        self.setGeometry(1500, 1000, 200, 100)
        self.setModal(True)  # 设置为模态窗口，阻塞其他窗口操作

        # 设置一个居中的提示标签
        label = QLabel("正在处理，请稍候 ...", self)
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        # 设置定时器
        QTimer.singleShot(int(step_time * 1000), self.close)
