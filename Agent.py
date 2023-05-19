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
        self.direction = 'down'
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
        if self.is_valid_move(next_row, next_col, game_coord):
            game_coord[next_row][next_col] = self.fire_bullet()
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
        else:
            return self.row, self.col

    def is_valid_move(self, row, col, game_coord):
        """
        检查移动是否有效

        Args:
            row (int): 目标位置的行
            col (int): 目标位置的列
            game_coord (List[List[int]]): 游戏空间的状态信息

        Returns:
            bool: 是否是有效移动
        """
        if row < 0 or row >= len(game_coord) or col < 0 or col >= len(game_coord[0]):
            return False  # 移动超出边界
        if game_coord[row][col] == 3:
            return False  # 移动到非空单元格
        return True

    def make_action(self, end,game_coord, target_bullets):
        """
        决定代理的下一步移动方向

        Args:
            game_coord (List[List[int]]): 游戏空间的状态信息

        Returns:
            str: 移动方向 ('up', 'down', 'left', 'right')



        Usage:
            str = BFS(self.game_coord)
            str = DFS(self.game_coord)
            str = Astar(self.game_coord)
            str = greedy(self.game_coord)
            str = scaredConsiderEnemyBullets(self.game_coord)
            ...
            
            
        When finishing this, just pass str as the direction to move()
        Example:
            agent.move(agent.make_action(game_coord), game_coord)
                
        """
        action = greedy(self,end,game_coord, target_bullets)
        self.move(action,game_coord)
                
    def fire_bullet(self):
        """
        发射子弹
        """
        return Bullet(self.row, self.col, self.direction , 1, "agent")
