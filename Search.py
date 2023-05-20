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

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        
from collections import deque

def BFS(start, end, game_coord, enemy_bullets):
    queue = deque([(start, [])])  # Queue to store positions and corresponding paths

    rows = len(game_coord)
    cols = len(game_coord[0])

    # Check if start and end positions are valid
    if game_coord[start.row][start.col] == 3 or game_coord[end.row][end.col] == 3:
        return "Invalid start or end position"

    # Define possible movements
    movements = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}

    # Create a visited grid to track visited positions
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    # BFS algorithm
    while queue:
        position, path = queue.popleft()  # Get the current position and path

        # Check if we reached the end position
        if position.row == end.row and position.col == end.col:
            # print("BFS tells you to go",path[0])
            return path[0]  # Return the shortest path as a list of actions

        # Check if the current position is valid and not visited
        if (
            0 <= position.row < rows and
            0 <= position.col < cols and
            not visited[position.row][position.col] and
            game_coord[position.row][position.col] != 3 and
            game_coord[position.row][position.col] != 6
        ):
            # Mark the current position as visited
            visited[position.row][position.col] = True

            # Explore possible movements
            for action, movement in movements.items():
                new_row = position.row + movement[0]
                new_col = position.col + movement[1]
                new_position = Position(new_row, new_col)
                new_path = path + [action]  # Add the current action to the path

                # Push the new position and path onto the queue
                queue.append((new_position, new_path))

    return "No path found"  # Return if no path is found


def DFS(start, end, game_coord, enemy_bullets):
    stack = [(start, [])]  # Stack to store positions and corresponding paths

    rows = len(game_coord)
    cols = len(game_coord[0])

    # Check if start and end positions are valid
    if game_coord[start.row][start.col] == 3 or game_coord[end.row][end.col] == 3:
        return "Invalid start or end position"

    # Define possible movements
    movements = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}

    # Create a visited grid to track visited positions
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    # DFS algorithm
    while stack:
        position, path = stack.pop()  # Get the current position and path

        # Check if we reached the end position
        if position.row == end.row and position.col == end.col:
            # print("DFS tells you to go",path[0])
            return path[0]  # Return the path as a list of actions

        # Check if the current position is valid and not visited
        if (
            0 <= position.row < rows and
            0 <= position.col < cols and
            not visited[position.row][position.col] and
            game_coord[position.row][position.col] != 3 and
            game_coord[position.row][position.col] != 6
        ):
            # Mark the current position as visited
            visited[position.row][position.col] = True

            # Explore possible movements
            for action, movement in movements.items():
                new_row = position.row + movement[0]
                new_col = position.col + movement[1]
                new_position = Position(new_row, new_col)
                new_path = path + [action]  # Add the current action to the path

                # Push the new position and path onto the stack
                stack.append((new_position, new_path))

    return "No path found"  # Return if no path is found




from queue import PriorityQueue

class Node:
    def __init__(self, position, g_score, h_score, parent=None):
        self.position = position
        self.g_score = g_score
        self.h_score = h_score
        self.f_score = g_score + h_score
        self.parent = parent

    def __lt__(self, other):
        return self.f_score < other.f_score

def calculate_manhattan_distance(curr_position, end_position):
    return abs(curr_position.row - end_position.row) + abs(curr_position.col - end_position.col)

def reconstruct_path(node):
    path = []
    current = node
    while current is not None:
        if current.parent is not None:
            direction = get_direction(current.parent.position, current.position)
            path.append(direction)
        current = current.parent
    path.reverse()
    return path

def get_direction(curr_position, next_position):
    row_diff = next_position.row - curr_position.row
    col_diff = next_position.col - curr_position.col
    if row_diff == -1:
        return 'up'
    elif row_diff == 1:
        return 'down'
    elif col_diff == -1:
        return 'left'
    elif col_diff == 1:
        return 'right'

def Astar(start,end,game_coord,enemy_bullets):
    rows = len(game_coord)
    cols = len(game_coord[0])

    # Check if start and end positions are valid
    if game_coord[start.row][start.col] == 3 or game_coord[end.row][end.col] == 3:
        return "Invalid start or end position"

    # Define possible movements
    movements = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}

    # Create a visited grid to track visited positions
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    # Priority queue to store nodes based on f-score
    open_set = PriorityQueue()
    
    # Create the start node
    start_node = Node(start, 0, calculate_manhattan_distance(start, end))
    open_set.put(start_node)

    # A* algorithm
    while not open_set.empty():
        curr_node = open_set.get()
        curr_position = curr_node.position

        # Check if we reached the end position
        if curr_position.row == end.row and curr_position.col == end.col:
            
            path = reconstruct_path(curr_node)  # Return the shortest path as a list of actions
            # print("Astar tells you to go",path[0])
            return path[0]
        # Check if the current position is valid and not visited
        if (
            0 <= curr_position.row < rows and
            0 <= curr_position.col < cols and
            not visited[curr_position.row][curr_position.col] and
            game_coord[curr_position.row][curr_position.col] != 3 and
            game_coord[curr_position.row][curr_position.col] != 6
        ):
            # Mark the current position as visited
            visited[curr_position.row][curr_position.col] = True

            # Explore possible movements
            for action, movement in movements.items():
                new_row = curr_position.row + movement[0]
                new_col = curr_position.col + movement[1]
                new_position = Position(new_row, new_col)

                # Calculate the new g-score and h-score for the neighbor node
                new_g_score = curr_node.g_score + 1  # Assuming a constant cost of 1 for each movement
                new_h_score = calculate_manhattan_distance(new_position, end)
                new_f_score = new_g_score + new_h_score

                # Create the neighbor node
                neighbor_node = Node(new_position, new_g_score, new_h_score, parent=curr_node)

                # Push the neighbor node onto the priority queue
                open_set.put(neighbor_node)

    return "No path found"  # Return if no path is found

def greedy_random(start,end,game_coord,enemy_bullets):
    dx = start.col - end.col
    dy = start.row - end.row
    if random.random()<0.5:
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
