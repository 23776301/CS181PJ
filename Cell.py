from Cell import *
from Agent import *
from Target import *
from Bullet import *
from MainGame import *
from Search import *
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
        
        """
        # 游戏空间：
        # 0 = 空，
        # 1 = 代理，
        # 2 = 目标，
        # 3 = 墙，
        # 4 = 代理子弹，
        # 5 = 目标子弹。
        # 6 = 代理大本营
        # 14 = 代理子弹+agent
        # 25 = 目标子弹+target
        """
        if self.cellstate==0:
            canvas.create_rectangle(x1, y1, x2, y2, fill="white")
        elif self.cellstate==3:
            canvas.create_rectangle(x1, y1, x2, y2, fill="black")
        elif self.cellstate==6:
            canvas.create_rectangle(x1, y1, x2, y2, fill="red")

        elif self.cellstate==1:
            canvas.create_oval(x1, y1, x2, y2, fill="red")
        elif self.cellstate==2:
            canvas.create_oval(x1, y1, x2, y2, fill="blue")
        elif self.cellstate==4:
            canvas.create_oval(x3-cell_size/6, y3-cell_size/6, x3+cell_size/6, y3+cell_size/6, fill="red")
        elif self.cellstate==5:
            canvas.create_oval(x3-cell_size/6, y3-cell_size/6, x3+cell_size/6, y3+cell_size/6, fill="blue")

        elif self.cellstate==14:
            canvas.create_oval(x1, y1, x2, y2, fill="red")
            canvas.create_oval(x3-cell_size/6, y3-cell_size/6, x3+cell_size/6, y3+cell_size/6, fill="red")
        elif self.cellstate==25:
            canvas.create_oval(x1, y1, x2, y2, fill="blue")
            canvas.create_oval(x3-cell_size/6, y3-cell_size/6, x3+cell_size/6, y3+cell_size/6, fill="blue")
        