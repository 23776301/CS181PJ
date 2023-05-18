import tkinter as tk
from tkinter import messagebox


class Cell:
    def __init__(self, row, col,cell_state):
        """
        每个单元格的表示和状态信息

        Args:
            row (int): 单元格所在的行
            col (int): 单元格所在的列
        """
        self.row = row
        self.col = col
        # 游戏空间：0 = 空，1 = 代理，2 = 目标，3 = 墙，4 = 代理子弹，5 = 目标子弹。
        self.cellstate = cell_state

    def draw(self, canvas, cell_size):
        """
        在画布上绘制单元格

        Args:
            canvas (tkinter.Canvas): 画布对象
            cell_size (int): 单元格的大小
        """
        x1 = self.col * cell_size
        y1 = self.row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size
        
        # bullet: half size
        x3 = x1 + cell_size/2
        y3 = y1 + cell_size/2
        
        
        # 游戏空间：
        # 0 = 空，
        # 1 = 代理，
        # 2 = 目标，
        # 3 = 墙，
        # 4 = 代理子弹，
        # 5 = 目标子弹。
        # 14 = 代理子弹+agent
        # 25 = 目标子弹+target
        if self.cellstate==0:
            canvas.create_rectangle(x1, y1, x2, y2, fill="white")
        elif self.cellstate==3:
            canvas.create_rectangle(x1, y1, x2, y2, fill="black")
            
        elif self.cellstate==1:
            canvas.create_oval(x1, y1, x2, y2, fill="red")
        elif self.cellstate==2:
            canvas.create_oval(x1, y1, x2, y2, fill="blue")
        elif self.cellstate==4:
            canvas.create_oval(x3-cell_size/3, y3-cell_size/3, x3+cell_size/3, y3+cell_size/3, fill="red")
        elif self.cellstate==5:
            canvas.create_oval(x3-cell_size/3, y3-cell_size/3, x3+cell_size/3, y3+cell_size/3, fill="blue")
        
        elif self.cellstate==14:
            canvas.create_oval(x1, y1, x2, y2, fill="red")
            canvas.create_oval(x3-cell_size/3, y3-cell_size/3, x3+cell_size/3, y3+cell_size/3, fill="red")
        elif self.cellstate==25:
            canvas.create_oval(x1, y1, x2, y2, fill="blue")
            canvas.create_oval(x3-cell_size/3, y3-cell_size/3, x3+cell_size/3, y3+cell_size/3, fill="blue")
            
            


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
        else:
            return self.row, self.col

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

    def get_action(self, game_space):
        """
        决定代理的下一步移动方向

        Args:
            game_space (List[List[int]]): 游戏空间的状态信息

        Returns:
            str: 移动方向 ('up', 'down', 'left', 'right')
        """
        while True:
            action = input("请输入移动方向(WASD或上下左右): ").lower()
            if action == "w" or action == "up":
                if self.is_valid_move(self.row - 1, self.col, game_space):
                    return "up"
            elif action == "s" or action == "down":
                if self.is_valid_move(self.row + 1, self.col, game_space):
                    return "down"
            elif action == "a" or action == "left":
                if self.is_valid_move(self.row, self.col - 1, game_space):
                    return "left"
            elif action == "d" or action == "right":
                if self.is_valid_move(self.row, self.col + 1, game_space):
                    return "right"
            else:
                print("无效的移动方向，请重新输入！")
                
    def fire_bullet(self):
        """
        发射子弹
        """
        return Bullet(self.row, self.col, self.direction , 1, "agent")


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
    
    def get_action(self):
        """
        决定目标的下一步移动方向

        Returns:
            str: 移动方向 ('up', 'down', 'left', 'right')
        """
        return "down"  # 替换为使用 BFS、DFS、A*、greedy 等算法决定下一步移动方向的逻辑
    def fire_bullet(self):
        """
        发射子弹
        """
        return Bullet(self.row, self.col, self.direction , 1, "target")

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

class Game:
    def __init__(self, width, height):
        """
        游戏的表示和状态信息

        Args:
            width (int): 游戏的宽度（列数）
            height (int): 游戏的高度（行数）
        """
        self.width = width
        self.height = height

        self.root = tk.Tk()
        self.root.title("射击游戏")

        self.cell_size = 30
        self.game_space = [[0 for _ in range(width)] for _ in range(height)]
        self.game_space[2][2] = 3

        self.agent = Agent(0, 0)
        self.target = Target(height - 1, width - 1)
        self.agent_bullets:list[Bullet] = []
        self.target_bullet:list[Bullet] = []
        self.update_game_space()
        
    def update_game_space(self):
        # if not wall, clear to 0
        for row in range(self.height):
            for col in range(self.width):
                if self.game_space[row][col] != 3:
                    self.game_space[row][col] = 0
        # if bullet, set to 4 or 5
        if self.agent_bullets is not None:
            for bullet in self.agent_bullets:
                self.game_space[bullet.row][bullet.col] = 4
        if self.target_bullet is not None:
            for bullet in self.target_bullet:
                self.game_space[bullet.row][bullet.col] = 5
        
        # if agent, set to 1 or 14
        if self.game_space[self.agent.row][self.agent.col] == 4:
            self.game_space[self.agent.row][self.agent.col] = 14
        else:
            self.game_space[self.agent.row][self.agent.col] = 1
        # if target, set to 2 or 25
        if self.game_space[self.target.row][self.target.col] == 5:
            self.game_space[self.target.row][self.target.col] = 25
        else:
            self.game_space[self.target.row][self.target.col] = 2
        
        # print(self.game_space)



    def draw(self):
        self.canvas.delete("all")  # 清空画布

        for row in range(self.height):
            for col in range(self.width):
                cell = Cell(row, col,self.game_space[row][col])
                cell.draw(self.canvas, self.cell_size)        

    def key_press(self, event):
        """
        键盘按下事件处理函数
        """
        key = event.keysym.lower()
        # if key:
            
        # 1, move bullets first
        if self.agent_bullets is not None:
            for a_b in self.agent_bullets:
                a_b.bullet_move_result(self.game_space)
        if self.target_bullet is not None:
            for t_b in self.target_bullet:
                t_b.bullet_move_result(self.game_space)
        
        # 2, check if anyone die
        #     if self.agent_bullets is not None:
        #         self.agent_bullets.move()
        #         self.agent_bullets.draw(self.canvas, self.cell_size)

        #         if self.agent_bullets.row < 0 or self.agent_bullets.row >= self.height or self.agent_bullets.col < 0 or self.agent_bullets.col >= self.width:
        #             self.agent_bullets = None
        #         elif self.agent_bullets.row == self.target.row and self.agent_bullets.col == self.target.col:
        #             messagebox.showinfo("游戏结束", "目标被击中！")
        #             self.root.quit()

        #     if self.target_bullet is not None:
        #         self.target_bullet.move()
        #         self.target_bullet.draw(self.canvas, self.cell_size)

        #         if self.target_bullet.row < 0 or self.target_bullet.row >= self.height or self.target_bullet.col < 0 or self.target_bullet.col >= self.width:
        #             self.target_bullet = None
        #         elif self.target_bullet.row == self.agent.row and self.target_bullet.col == self.agent.col:
        #             messagebox.showinfo("游戏结束", "代理被击中！")
        #             self.root.quit()

        
        
        
        
        
        # 3, use keyboard or AI to get action and move agent and target
        
        
        if key == "up":
            self.agent.move("up", self.game_space)
        elif key == "down":
            self.agent.move("down", self.game_space)
        elif key == "left":
            self.agent.move("left", self.game_space)
        elif key == "right":
            self.agent.move("right", self.game_space)
        
        
        
        
        
        # 4, fire bullets
        self.agent_bullets.append(self.agent.fire_bullet())
        self.target_bullet.append(self.target.fire_bullet())
        
        self.update_game_space()
            
        print(self.game_space)  

        self.draw()

    def run(self):
        """
        运行游戏
        """
        self.canvas = tk.Canvas(self.root, width=self.width * self.cell_size, height=self.height * self.cell_size)
        self.canvas.pack()

        self.draw()

        self.root.bind("<KeyPress>", self.key_press)
        self.root.mainloop()

game = Game(20, 20)
game.run()