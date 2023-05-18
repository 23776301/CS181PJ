from Cell import *
from Agent import *
from Target import *
from Bullet import *
from MainGame import *
from Search import *
class Bullet:
    def __init__(self, row, col, direction, speed, owner):
        """
        子弹的表示和状态信息

        Args:
            row (int): 子弹所在的行
            col (int): 子弹所在的列
            direction (str): 子弹移动的方向 ('up', 'down', 'left', 'right')
            speed (int): 子弹移动的速度（单元格数）
        """
        self.row = row
        self.col = col
        self.direction = direction
        self.speed = speed
        self.owner = owner
    def get_next_position(self, direction):
        """
        获取下一个位置的行和列

        Args:
            direction (str): 移动方向 ('up', 'down', 'left', 'right')

        Returns:
            Tuple[int, int]: 下一个位置的行和列
        """
        if direction == "up":
            return self.row - 1, self.col
        elif direction == "down":
            return self.row + 1, self.col
        elif direction == "left":
            return self.row, self.col - 1
        elif direction == "right":
            return self.row, self.col + 1
    def bullet_move_result(self, game_space):
        """
        0. normal, move onto empty cell
        1. hit wall, bounce back
        2. someone die, end the game
        3. 
        """
        next_row, next_col = self.get_next_position(self.direction)
        if (
            next_row < 0
            or next_row >= len(game_space)
            or next_col < 0
            or next_col >= len(game_space[0])
        ):
            # out of map
            return -1
        
        next_cell = game_space[next_row][next_col]

        if next_cell == 0:
            # Case 0: Normal move onto an empty cell
            self.bullet_normal_move(game_space)
            return 0
        elif next_cell == 3:
            # Case 1: Hit a wall, bounce back
            if self.direction == "up":
                self.direction = "down"
            elif self.direction == "down":
                self.direction = "up"
            elif self.direction == "left":
                self.direction = "right"
            elif self.direction == "right":
                self.direction = "left"
            return 1
        elif next_cell == 1 and self.owner == "target":
            # Case 2: target kills agent, end the game
            return 2
        elif next_cell == 2 and self.owner == "agent":
            # Case 3: agent kills target, end the game
            return 3
        else:
            self.bullet_normal_move(game_space)
            return 0
        
        
    def bullet_normal_move(self,game_space):
        if self.direction == "up":
            self.row -= self.speed
        elif self.direction == "down":
            self.row += self.speed
        elif self.direction == "left":
            self.col -= self.speed
        elif self.direction == "right":
            self.col += self.speed

        game_space[self.row][self.col] = self
