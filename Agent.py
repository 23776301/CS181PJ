from Cell import *
from Agent import *
from Target import *
from Bullet import *
from MainGame import *
from Search import *


class Agent:
    def __init__(self, row, col):
        """
        代理的表示和状态信息

        Args:
            row (int): 代理所在的行
            col (int): 代理所在的列
        """
        self.row = row
        self.col = col
        self.direction = "down"
        # 游戏空间：
        # 0 = 空，
        # 1 = 代理，
        # 2 = 目标，
        # 3 = 墙，
        # 4 = 代理子弹，
        # 5 = 目标子弹。
        # 14 = 代理子弹+agent
        # 25 = 目标子弹+target

    def move(self, direction, game_coord):
        self.direction = direction
        next_row, next_col = self.get_next_position(direction)
        # print("agent moving to",next_row, next_col, "state " , game_coord[next_row][next_col])
        if (
            next_row < 0
            or next_row >= len(game_coord)
            or next_col < 0
            or next_col >= len(game_coord[0])
        ):
            # out of map, keep still, do nothing
            return "out of map"

        elif game_coord[next_row][next_col] == 0:
            # safe step. go normally
            self.row = next_row
            self.col = next_col
            game_coord[self.row][self.col] = 1
            abullet = self.fire_bullet(game_coord)
            return abullet

        elif game_coord[next_row][next_col] == 1:
            # ?? never happen 2 agents in the game
            return "impolite scene"

        elif game_coord[next_row][next_col] == 2:
            # move towards target
            return "hit enemy"

        elif game_coord[next_row][next_col] == 3:
            # hit wall, keep still
            return "hit wall"

        elif game_coord[next_row][next_col] == 4:
            self.row = next_row
            self.col = next_col
            game_coord[self.row][self.col] = 14
            # abullet = self.fire_bullet(game_coord)
            # return abullet
            return "hit own bullet"

        elif game_coord[next_row][next_col] == 5:
            # agent killed by target bullet
            return "hit enemy's bullet"

    def get_next_position(self, direction):
        if direction == "up":
            return self.row - 1, self.col
        elif direction == "down":
            return self.row + 1, self.col
        elif direction == "left":
            return self.row, self.col - 1
        elif direction == "right":
            return self.row, self.col + 1
        elif direction == None:  # no direction ?
            return self.row, self.col
        else:  # no direction ?
            return self.row, self.col

    def make_action(self, end, game_coord, target_bullets):
        action = greedy_random(self, end, game_coord, target_bullets)
        return self.move(action, game_coord)

    def fire_bullet(self,game_coord):
        # print("agent fire at ", self.row, self.col, "direction ", self.direction, "state ", game_coord[self.row][self.col])
        """
        发射子弹
        """
        if game_coord[self.row][self.col] == 1:
            game_coord[self.row][self.col] = 14
            return Bullet(self.row, self.col, self.direction, 1, "agent")
        else:
            return 'cannot store 2 bullets in one cell'
