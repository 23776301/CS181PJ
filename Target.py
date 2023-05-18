from Cell import *
from Agent import *
from Target import *
from Bullet import *
from MainGame import *
from Search import *
class Target:
    def __init__(self, row, col):
        """
        目标的表示和状态信息

        Args:
            row (int): 目标所在的行
            col (int): 目标所在的列
        """
        self.row = row
        self.col = col
        self.direction = 'up'
    def move(self, direction, game_space):
        self.direction = direction
        next_row, next_col = self.get_next_position(direction)
        if self.is_valid_move(next_row, next_col, game_space):
            game_space[next_row][next_col] = self.fire_bullet()
            self.row = next_row
            self.col = next_col


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

    def is_valid_move(self, row, col, game_space):
        """
        检查移动是否有效

        Args:
            row (int): 目标位置的行
            col (int): 目标位置的列
            game_space (List[List[int]]): 游戏空间的状态信息

        Returns:
            bool: 是否是有效移动
        """
        if row < 0 or row >= len(game_space) or col < 0 or col >= len(game_space[0]):
            return False  # 移动超出边界
        if game_space[row][col] == 3:
            return False  # 移动到非空单元格
        return True
    
    def make_action(self,game_space):
        """
        决定目标的下一步移动方向

        Returns:
            str: 移动方向 ('up', 'down', 'left', 'right')
        """
        self.move('up',game_space)
    def fire_bullet(self):
        """
        发射子弹
        """
        return Bullet(self.row, self.col, self.direction , 1, "target")
