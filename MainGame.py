from Cell import *
from Agent import *
from Target import *
from Bullet import *
from MainGame import *
from Search import *
from CollectScores import collect_score
import tkinter as tk
from tkinter import messagebox
import random
# import Agent.py, Bullet, Target, Cell
from Agent import *
from Bullet import *
from Target import *
from Cell import *
import sys
# When set to False, you can press any key
#       to see two AIs playing.
#       NOTE that if you press and holding for too long,
#       you will miss out many beautiful sights
USE_KEYBOARD = False

class Game:
    def __init__(self, width, height, size, GUI_interval, cut):
        """
        游戏的表示和状态信息

        Args:
            width (int): 游戏的宽度（列数）
            height (int): 游戏的高度（行数）
        """
        self.cut = cut
        self.width = width
        self.height = height
        self.quit = False
        self.root = tk.Tk()
        self.GUI_interval = GUI_interval
        # disable GUI
        if GUI_interval == '0':
            self.root.withdraw()
        else:
            self.GUI_interval = GUI_interval
        self.root.title(" Defend Our Home ! ")
        self.score = 0
        self.step = 0

        self.cell_size = size
        self.game_coord = [[0 for _ in range(width)] for _ in range(height)]

        self.set_cell(1, round(self.width/3), 6) # 设置我方大本营位置
        self.agentHome = Position(1,round(self.width/3))
        # print(self.game_coord)
        self.agent = Agent(0, 0)
        self.target = Target(height - 1, width - 1)
        # self.target_path_bfs = enemy_BFS(self.target, (1, 1), self.game_coord) # 假设敌方坦克会根据bfs找到袭击的最短路径，该路径存储在列表中
        # print(self.target_path_bfs)
                
        self.agent_bullets:list[Bullet] = []
        self.target_bullets:list[Bullet] = []        
        for row in range(height):
            for col in range(width):
                self.set_random_game_coord(row,col,0.2)
        self.update_game_coord()
        
    def set_cell(self, row, col, value):
        self.game_coord[row][col] = value

    # every cell has possibility P to be a wall
    def set_random_game_coord(self,row,col,P):
        if random.random()<P:
            self.set_cell(row,col,3)
        else:
            self.set_cell(row,col,0)
        self.update_game_coord()
        if self.check_valid_coord() == False:
            self.set_random_game_coord(row,col,P)
        
    def check_valid_coord(self):
        # print(BFS(self.agent, self.target, self.game_coord, self.target_bullets))
        # print(BFS(self.target, self.agentHome, self.game_coord, self.agent_bullets))
        if BFS(self.agent, self.target, self.game_coord, self.target_bullets) == "No path found":
            return False
        if BFS(self.target, self.agentHome, self.game_coord, self.agent_bullets) == "No path found":
            return False
        return True
    def update_game_coord(self):
        # print("\nagent bullet\n",self.agent_bullets,"\ntarget_bullets\n",self.target_bullets)
        # if not wall, clear to 0
        
        # print(self.game_coord)
        for row in range(self.height):
            for col in range(self.width):
                if self.game_coord[row][col] != 3 and self.game_coord[row][col] != 6:
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
            
            
        self.set_cell(1, round(self.width/3), 6) # 设置我方大本营位置
        # 设置我方大本营位置 again, in case it was overrided by bullets
        
        # print(self.game_coord)
    def check_collision(self):
        if self.agent.row == self.target.row and self.agent.col == self.target.col:
            self.score+=100
            messagebox.showinfo("Game Ends!", 'Home protected successfully!')
            print(self.score)
            self.quit = True
            self.root.quit()
        if self.target.row == 1 and self.target.col == 1:
            self.score-=100
            messagebox.showinfo("Game Ends!", "home attacked!")
            print(self.score)
            self.quit = True
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
                # elif (result == 2):# target kills agent, end the game
                #     self.score-=100
                #     messagebox.showinfo("Game Ends!", "agent was killed!")
                # print(self.score)    
                # self.root.quit()
                    
                    
        if len(self.target_bullets) > 0:
            for a_b in self.agent_bullets:
                # print(a_b.row,a_b.col,a_b.direction,a_b.speed,a_b.owner)
                result = a_b.bullet_move_result(self.game_coord)
                if (result == -1):# out of map
                    self.agent_bullets.remove(a_b)
                # elif (result == 3):# agent kills target, end the game
                #     self.score+=100
                #     messagebox.showinfo("Game Ends!", "target was killed!")
                # print(self.score)    
                # self.root.quit()
        self.update_game_coord()

        self.step += 1

        # 检查碰撞
        # This actually doesn't work. If do not believe, 
        #       comment off other "Home protected successfully!" adn related lines, to check whether the line below works
        self.check_collision()
        
        if(USE_KEYBOARD):
            if key == "up":
                agent_move_result = self.agent.move("up", self.game_coord)
            elif key == "down":
                agent_move_result = self.agent.move("down", self.game_coord)
            elif key == "left":
                agent_move_result = self.agent.move("left", self.game_coord)
            elif key == "right":
                agent_move_result = self.agent.move("right", self.game_coord)
            else:
                agent_move_result = self.agent.move(None, self.game_coord)
        else:
            if self.score > - self.cut:
                agent_move_result = self.agent.make_action(self.target,self.agentHome,self.game_coord,self.target_bullets)
            else:
                agent_move_result = self.agent.make_action_less_time_left(self.target,self.agentHome,self.game_coord,self.target_bullets)
        # check move cause what
        if agent_move_result == 'hit enemy':
            self.score += 100
            # messagebox.showinfo("Game Ends!", agent_move_result)
            # messagebox.showinfo("Game Ends!", 'Home protected successfully!')
            print(self.score)
            self.quit = True
            self.root.quit()
        # elif agent_move_result == "hit enemy's bullet":
        #     self.score -= 200
        #     messagebox.showinfo("Game Ends!", agent_move_result)
        # print(self.score)    
        # self.root.quit()

        if self.score <= -100:
            print(self.score)
            self.quit = True
            self.root.quit()
        if (self.quit):
            return
        # target 沿求得最短路径前进
        # npos = self.target_path_bfs[self.step]
        # self.target = Target(npos[0], npos[1])
        #  use AI to get action and move target
        # NOTE NOTE: You can specify the make_action()'s start and end position,
        #  while start do not need to pass into, 
        #  because python class passes the caller class object itself as the default first parameter
        if self.score > -50:
            target_move_result = self.target.make_action(self.agent,self.agentHome,self.game_coord,self.agent_bullets)
        else:
            target_move_result = self.target.make_action_less_time_left(self.agent,self.agentHome,self.game_coord,self.target_bullets)
        # print(target_move_result)
        # check move cause what
        if target_move_result == 'hit agent':
            self.score += 100
            # messagebox.showinfo("Game Ends!", target_move_result)
            # messagebox.showinfo("Game Ends!", 'Home protected successfully!')
            print(self.score)
            self.quit = True
            self.root.quit()
        elif target_move_result == "destory home!":
            self.score -= 100
            # messagebox.showinfo("Game Ends!", target_move_result)
            print(self.score)
            self.quit = True
            self.root.quit()
        # elif target_move_result == "hit agent's bullet":
        #     self.score += 200
        #     messagebox.showinfo("Game Ends!", target_move_result)
        # print(self.score)    
        # self.root.quit()
        

        self.check_collision()
        self.score-=1
        
        
        
        # self.update_game_coord()  
        # 4, fire bullets
        # print("agent_move_result",agent_move_result)
        # print("target_move_result",target_move_result)
        agent_fire_result = agent_move_result
        if type(agent_fire_result) == Bullet:
            self.agent_bullets.append(agent_fire_result)
        target_fire_result = target_move_result
        if type(target_fire_result) == Bullet:
            self.target_bullets.append(target_fire_result)
        
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
    
    def autokeyinput(self):
        event = tk.Event()
        event.keysym = 'space'
        self.key_press(event)
        self.root.after(int(self.GUI_interval), self.autokeyinput)

    def run_auto(self):
        """
        运行游戏
        """
        self.canvas = tk.Canvas(self.root, width=self.width * self.cell_size, height=self.height * self.cell_size)
        self.canvas.pack()

        self.draw()
        self.autokeyinput()
        self.root.mainloop()

if __name__ == "__main__":
    arg1 = int(sys.argv[1])
    arg2 = int(sys.argv[2])
    game = Game(30, 20, 30, arg1,arg2)
    game.run_auto()