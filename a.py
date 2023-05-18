import random
import time
import os

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

    # 更新敌方位置
    if enemy_x > player_x:
        enemy_x -= enemy_speed
    elif enemy_x < player_x:
        enemy_x += enemy_speed
    if enemy_y > player_y:
        enemy_y -= enemy_speed
    elif enemy_y < player_y:
        enemy_y += enemy_speed

    # 敌方发射子弹
    if random.randint(0, 100) < 10:
        bullet = (enemy_x, enemy_y)
        bullets.append(bullet)

    # 移动子弹
    bullets = [(x, y-1) for (x, y) in bullets]

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
