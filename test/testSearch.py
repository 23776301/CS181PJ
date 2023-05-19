def DFS(start, end, game_coord):
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
            return path  # Return the path as a list of actions

        # Check if the current position is valid and not visited
        if (
            0 <= position.row < rows and
            0 <= position.col < cols and
            not visited[position.row][position.col] and
            game_coord[position.row][position.col] != 3
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


from collections import deque

def BFS(start, end, game_coord):
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
            return path  # Return the shortest path as a list of actions

        # Check if the current position is valid and not visited
        if (
            0 <= position.row < rows and
            0 <= position.col < cols and
            not visited[position.row][position.col] and
            game_coord[position.row][position.col] != 3
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


from queue import PriorityQueue

class Node:
    def __init__(self, position, g_score, h_score):
        self.position = position
        self.g_score = g_score
        self.h_score = h_score
        self.f_score = g_score + h_score

    def __lt__(self, other):
        return self.f_score < other.f_score

def calculate_manhattan_distance(curr_position, end_position):
    return abs(curr_position.row - end_position.row) + abs(curr_position.col - end_position.col)

def Astar(start, end, game_coord):
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
            return curr_node.f_score  # Return the shortest path length

        # Check if the current position is valid and not visited
        if (
            0 <= curr_position.row < rows and
            0 <= curr_position.col < cols and
            not visited[curr_position.row][curr_position.col] and
            game_coord[curr_position.row][curr_position.col] != 3
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
                neighbor_node = Node(new_position, new_g_score, new_h_score)

                # Push the neighbor node onto the priority queue
                open_set.put(neighbor_node)

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

def Astar(start, end, game_coord):
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
            return reconstruct_path(curr_node)  # Return the shortest path as a list of actions

        # Check if the current position is valid and not visited
        if (
            0 <= curr_position.row < rows and
            0 <= curr_position.col < cols and
            not visited[curr_position.row][curr_position.col] and
            game_coord[curr_position.row][curr_position.col] != 3
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

# Example usage
game_coord = [
    [0, 0, 0, 0],
    [0, 3, 3, 0],
    [0, 0, 0, 0],
    [3, 3, 0, 0],
    [0, 0, 0, 0]
]

class Position:
    def __init__(self,row,col):
        self.col = col
        self.row = row
        
start = Position(0,0)
end = Position(3,3)

path = Astar(start, end,game_coord)

if path:
    print("Path found:", path)
else:
    print("Path not found.")

