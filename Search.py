from Cell import *
from Agent import *
from Target import *
from Bullet import *
from MainGame import *
from Search import *
from collections import deque

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
MAX_VALUE = 0x7fffffff
def enemy_BFS(start,end,game_coord):
    n, m = len(game_coord), len(game_coord[0])
    dist = [[MAX_VALUE for _ in range(m)] for _ in range(n)] # 标记每个点在第几层被搜索
    pre = [[None for _ in range(m)] for _ in range(n)]  # 记录所在点的上一个点
    actions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    sx, sy = start.row, start.col
    gx, gy = end[0], end[1]

    dist[sx][sy] = 0
    queue = deque()
    # queue.append((start.x, start.y), None)
    queue.append((start.row, start.col))
    while queue:
        curr = queue.popleft()
        find = False
        for i in range(4):
            nx, ny = curr[0] + actions[i][0], curr[1] + actions[i][1]
            if (0 <= nx < n) and (0 <= ny < m) and (game_coord[nx][ny] != 3) and (dist[nx][ny] == MAX_VALUE):
                dist[nx][ny] = dist[curr[0]][curr[1]] + 1
                pre[nx][ny] = curr
                queue.append((nx, ny))
                if nx == gx and ny == gy:
                    find = True
                    break

        if find:
            while queue:
                curr = queue.popleft()
            stack = []
            curr = end
            while True:
                stack.append(curr)
                if curr[0] == start.row and curr[1] == start.col:
                    break
                prev = pre[curr[0]][curr[1]]
                curr = prev
            return list(reversed(stack))
    return []

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