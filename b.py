import random
import time
import os
from collections import deque

# 游戏窗口的宽度和高度
window_width = 30
window_height = 20

# 玩家初始位置和移动速度
player_x = 1
player_y = 1
player_speed = 1

# 敌方初始位置和移动速度
enemy_x = window_width - 2
enemy_y = window_height - 2
enemy_speed = 1

# 子弹列表
bullets = []

# 食物列表
foods = []
food_count = 10

# 创建食物
for _ in range(food_count):
    food_x = random.randint(1, window_width - 2)
    food_y = random.randint(1, window_height - 2)
    foods.append((food_x, food_y))

# 游戏结束标志
game_over = False

# BFS搜索函数
def bfs_search(start_pos, target_pos):
    queue = deque([(start_pos, [])])
    visited = set()

    while queue:
        current_pos, path = queue.popleft()
        x, y = current_pos

        if current_pos == target_pos:
            return path

        if current_pos in visited:
            continue

        visited.add(current_pos)

        # 检查上方格子
        if y > 0:
            queue.append(((x, y - 1), path + ['up']))

        # 检查下方格子
        if y < window_height - 1:
            queue.append(((x, y + 1), path + ['down']))

        # 检查左方格子
        if x > 0:
            queue.append(((x - 1, y), path + ['left']))

        # 检查右方格子
        if x < window_width - 1:
            queue.append(((x + 1, y), path + ['right']))

    return []

# 游戏循环
while not game_over:
    # 清空终端窗口
    os.system('cls' if os.name == 'nt' else 'clear')

    # 绘制游戏界面
    for y in range(window_height):
        for x in range(window_width):
            if (x, y) == (player_x, player_y):
                print('P', end='')
            elif (x, y) == (enemy_x, enemy_y):
                print('E', end='')
            elif (x, y) in bullets:
                print('*', end='')
            elif (x, y) in foods:
                print('F', end='')
            else:
                print(' ', end='')
        print()

    # 获取键盘输入
    direction = input("请输入移动方向（w上，s下，a左，d右）：")

    # 更新玩家位置
    if direction == 'w':
        player_y -= player_speed
    elif direction == 's':
        player_y += player_speed
    elif direction == 'a':
        player_x -= player_speed
    elif direction == 'd':
        player_x += player_speed

    # 使用BFS搜索玩家位置
    path_to_player = bfs_search((enemy_x, enemy_y), (player_x, player_y))
    if path_to_player:
        next_move = path_to_player[0]
        if next_move == 'up':
            enemy_y -= enemy_speed
        elif next_move == 'down':
            enemy_y += enemy_speed
        elif next_move == 'left':
            enemy_x -= enemy_speed
        elif next_move == 'right':
            enemy_x += enemy_speed

    # 敌方发射子弹
    if random.randint(0, 100) < 10:
        bullet = (enemy_x, enemy_y)
        bullets.append(bullet)

    # 移动子弹
    bullets = [(x, y - 1) for (x, y) in bullets]

    # 检测碰撞
    if (player_x, player_y) in bullets:
        game_over = True
    bullets = [(x, y) for (x, y) in bullets if y > 0]

    # 检查是否吃到食物
    if (player_x, player_y) in foods:
        foods.remove((player_x, player_y))

    # 判断游戏是否结束
    if len(foods) == 0:
        game_over = True

    # 控制游戏帧率
    time.sleep(0.1)

# 游戏结束，显示结果
os.system('cls' if os.name == 'nt' else 'clear')
if len(foods) == 0:
    print("恭喜你，吃完了所有的食物！")
else:
    print("游戏结束，你被击中了！")
