from Cell import *
from Agent import *
from Target import *
from Bullet import *
from MainGame import *
from Search import *

import tkinter as tk
from tkinter import messagebox
import random
# import Agent.py, Bullet, Target, Cell
from Agent import *
from Bullet import *
from Target import *
from Cell import *

USE_KEYBOARD = True

class Game:
    def __init__(self, width, height, size):
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
        self.score = 0

        self.cell_size = size
        self.game_coord = [[0 for _ in range(width)] for _ in range(height)]
        for row in range(height):
            for col in range(width):
                self.set_random_game_coord(row,col,0.02)


        self.agent = Agent(0, 0)
        self.target = Target(height - 1, width - 1)
        self.agent_bullets:list[Bullet] = []
        self.target_bullets:list[Bullet] = []
        self.update_game_coord()
        
    def set_cell(self, row, col, value):
        self.game_coord[row][col] = value

    # every cell has possibility P to be a wall
    def set_random_game_coord(self,row,col,P):
        if random.random()<P:
            self.set_cell(row,col,3)
        else:
            self.set_cell(row,col,0)
        
        
    def update_game_coord(self):
        # if not wall, clear to 0
        for row in range(self.height):
            for col in range(self.width):
                if self.game_coord[row][col] != 3:
                    self.game_coord[row][col] = 0
        # if bullet, set to 4 or 5
        if self.agent_bullets is not None:
            for bullet in self.agent_bullets:
                self.game_coord[bullet.row][bullet.col] = 4
        if self.target_bullets is not None:
            for bullet in self.target_bullets:
                self.game_coord[bullet.row][bullet.col] = 5
        
        # if agent, set to 1 or 14
        if self.game_coord[self.agent.row][self.agent.col] == 4:
            self.game_coord[self.agent.row][self.agent.col] = 14
        else:
            self.game_coord[self.agent.row][self.agent.col] = 1
        # if target, set to 2 or 25
        if self.game_coord[self.target.row][self.target.col] == 5:
            self.game_coord[self.target.row][self.target.col] = 25
        else:
            self.game_coord[self.target.row][self.target.col] = 2
        
        # print(self.game_coord)
    def check_collision(self):
        if self.agent.row == self.target.row and self.agent.col == self.target.col:
            self.score-=50
            messagebox.showinfo("游戏结束", "agent hit target!")
            self.root.quit()


    def draw(self):
        self.canvas.delete("all")  # 清空画布

        for row in range(self.height):
            for col in range(self.width):
                cell = Cell(row, col,self.game_coord[row][col])
                cell.draw(self.canvas, self.cell_size)        

    def key_press(self, event):
        """
        键盘按下事件处理函数
        """
        key = event.keysym.lower()
        # if key:
            
        #  move bullets first, check death
        if len(self.target_bullets) > 0:
            for t_b in self.target_bullets:
                result = t_b.bullet_move_result(self.game_coord)
                if (result == -1):# out of map
                    self.target_bullets.remove(t_b)
                elif (result == 2):# target kills agent, end the game
                    self.score-=100
                    messagebox.showinfo("游戏结束", "target was killed!")
                    self.root.quit()
                    
                    
        if len(self.target_bullets) > 0:
            for a_b in self.agent_bullets:
                # print(a_b.row,a_b.col,a_b.direction,a_b.speed,a_b.owner)
                result = a_b.bullet_move_result(self.game_coord)
                if (result == -1):# out of map
                    self.agent_bullets.remove(a_b)
                elif (result == 3):# agent kills target, end the game
                    self.score+=100
                    messagebox.showinfo("游戏结束", "target was killed!")
                    self.root.quit()
                    

        
        
        
        #  use keyboard or AI to get action and move agent and target

        self.target.make_action(self.agent,self.game_coord,self.agent_bullets)
        self.check_collision()
        
        if(USE_KEYBOARD):
            if key == "up":
                self.agent.move("up", self.game_coord)
            elif key == "down":
                self.agent.move("down", self.game_coord)
            elif key == "left":
                self.agent.move("left", self.game_coord)
            elif key == "right":
                self.agent.move("right", self.game_coord)
        else:
            self.agent.make_action(self.target,self.game_coord,self.target_bullets)

        self.check_collision()
        self.score-=1
        
        
        
              
        # self.update_game_coord()  
        # 4, fire bullets
        self.agent_bullets.append(self.agent.fire_bullet())
        self.target_bullets.append(self.target.fire_bullet())
        
        self.update_game_coord()
            
        # print(self.game_coord)  

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


if __name__ == "__main__":
    game = Game(50, 30, 15)
    game.run()