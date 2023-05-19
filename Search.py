from Cell import *
from Agent import *
from Target import *
from Bullet import *
from MainGame import *
from Search import *
"""
# 游戏空间：
# 0 = 空，
# 1 = 代理，
# 2 = 目标，
# 3 = 墙，
# 4 = 代理子弹，
# 5 = 目标子弹。
# 14 = 代理子弹+agent
# 25 = 目标子弹+target
"""
def BFS(start,end,game_coord,enemy_bullets):
    pass
def DFS(start,end,game_coord,enemy_bullets):
    pass
def Astar(start,end,game_coord,enemy_bullets):
    pass
def greedy(start,end,game_coord,enemy_bullets):
    dx = start.col - end.col
    dy = start.row - end.row
    if abs(dx) > abs(dy):
        if dx > 0:
            return 'left'
        else:
            return 'right'
    else:
        if dy > 0:
            return 'up'
        else:
            return 'down'
    
def scaredConsiderEnemyBullets(start,end,game_coord,enemy_bullets):
    pass
def braveConsiderEnemyBullets(start,end,game_coord,enemy_bullets):
    pass