import pygame
from sprites import *
import sys
import math
class TankWar:

    def __init__(self):
        self.screen = pygame.display.set_mode(Settings.SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.game_still = True
        self.hero = None
        self.enemies = None
        self.enemy_bullets = None
        self.walls = None

    @staticmethod
    def __init_game():
        """
        初始化游戏的一些设置
        :return:
        """
        pygame.init()   # 初始化pygame模块
        
        # pygame.event.set_grab(True)
        # pygame.mouse.set_visible(False)
        # if sys.platform.startswith('linux'):
        #     import subprocess
        #     subprocess.Popen(['wmctrl', '-a', 'Summary: Press SPACE to quit'])
        # if sys.platform == 'win32':
        #     import ctypes
        #     ctypes.windll.user32.SetForegroundWindow(pygame.display.get_wm_info()['window'])
        pygame.display.set_caption(Settings.GAME_NAME)  # 设置窗口标题
        pygame.mixer.init()    # 初始化音频模块

    def __create_sprite(self):
        self.hero = Hero(Settings.HERO_IMAGE_NAME, self.screen)
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.enemy_count = 1
        for i in range(self.enemy_count):
            direction = random.randint(0, 3)
            enemy = Enemy(Settings.ENEMY_IMAGES[direction], self.screen)
            enemy.direction = direction
            self.enemies.add(enemy)
        self.__draw_map()

    def __draw_map(self):
        """
        绘制地图
        :return:
        """
        for y in range(len(Settings.MAP_ONE)):
            for x in range(len(Settings.MAP_ONE[y])):
                if Settings.MAP_ONE[y][x] == 0:
                    continue
                wall = Wall(Settings.WALLS[Settings.MAP_ONE[y][x]], self.screen)
                wall.rect.x = x*Settings.BOX_SIZE
                wall.rect.y = y*Settings.BOX_SIZE
                if Settings.MAP_ONE[y][x] == Settings.RED_WALL:
                    wall.type = Settings.RED_WALL
                elif Settings.MAP_ONE[y][x] == Settings.IRON_WALL:
                    wall.type = Settings.IRON_WALL
                elif Settings.MAP_ONE[y][x] == Settings.WEED_WALL:
                    wall.type = Settings.WEED_WALL
                #elif Settings.MAP_ONE[y][x] == Settings.BOSS_WALL:
                #    wall.type = Settings.BOSS_WALL
                #    wall.life = 1
                self.walls.add(wall)

    def __check_keydown(self, event):
        """检查按下按钮的事件"""
        # self.hero.shot()
        if event.key == pygame.K_LEFT:
            # 按下左键
            self.hero.direction = Settings.LEFT
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
        elif event.key == pygame.K_RIGHT:
            # 按下右键
            self.hero.direction = Settings.RIGHT
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
        elif event.key == pygame.K_UP:
            # 按下上键
            self.hero.direction = Settings.UP
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
        elif event.key == pygame.K_DOWN:
            # 按下下键
            self.hero.direction = Settings.DOWN
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
            
    def __go_left(self):
        self.hero.direction = Settings.LEFT
        self.hero.is_moving = True
        self.hero.is_hit_wall = False
    def __go_right(self):
        self.hero.direction = Settings.RIGHT
        self.hero.is_moving = True
        self.hero.is_hit_wall = False
    def __go_up(self):
        self.hero.direction = Settings.UP
        self.hero.is_moving = True
        self.hero.is_hit_wall = False
    def __go_down(self):
        self.hero.direction = Settings.DOWN
        self.hero.is_moving = True
        self.hero.is_hit_wall = False
        
        
    import math

    def calculate_distance(self,pos1, pos2):
        """Calculate the Euclidean distance between two positions"""
        x1, y1 = pos1
        x2, y2 = pos2
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance

    def __AI_key_player(self):
    # """AI controller to greedy move the tank closer to the enemy"""
    # Calculate the distance between the tank and the enemy
        enemy_distance = self.calculate_distance(self.hero.rect.center, self.enemies.sprites()[0].rect.center)

        # Set the tank's direction towards the enemy based on the shortest distance
        if enemy_distance > 0:
            x_diff = self.enemies.sprites()[0].rect.centerx - self.hero.rect.centerx
            y_diff = self.enemies.sprites()[0].rect.centery - self.hero.rect.centery
            if abs(x_diff) > abs(y_diff):
                self.hero.direction = Settings.RIGHT if x_diff > 0 else Settings.LEFT
            else:
                self.hero.direction = Settings.DOWN if y_diff > 0 else Settings.UP
        else:
            # If the tank is already at the enemy's position, stop moving
            self.hero.is_moving = False

        # Update the tank's movement status
        self.hero.is_hit_wall = False
        self.hero.is_moving = True

        
        
        
        
        
        #elif event.key == pygame.K_SPACE:
            # 坦克发子弹
        #    self.hero.shot()

    # def __check_keyup(self, event):
    #     """检查松开按钮的事件"""
    #     if event.key == pygame.K_LEFT:
    #         # 松开左键
    #         self.hero.direction = Settings.LEFT
    #         self.hero.is_moving = False
    #     elif event.key == pygame.K_RIGHT:
    #         # 松开右键
    #         self.hero.direction = Settings.RIGHT
    #         self.hero.is_moving = False
    #     elif event.key == pygame.K_UP:
    #         # 松开上键
    #         self.hero.direction = Settings.UP
    #         self.hero.is_moving = False
    #     elif event.key == pygame.K_DOWN:
    #         # 松开下键
    #         self.hero.direction = Settings.DOWN
    #         self.hero.is_moving = False

    def __event_handler(self):
        
        if pygame.time.get_ticks() % 1000 == 0:
            TankWar.__AI_key_player(self)
        # Add your state update code here
        for event in pygame.event.get():
            # 判断是否是退出游戏
            if event.type == pygame.QUIT:
                TankWar.__game_over()
            # elif event.type == pygame.KEYDOWN:
                # TankWar.__check_keydown(self, event)
            # elif event.type == pygame.KEYUP:
            #     TankWar.__check_keyup(self, event)
    
    def __AI_handler(self):
        for event in pygame.event.get():
            # 判断是否是退出游戏
            if event.type == pygame.QUIT:
                TankWar.__game_over()
            else:
                # pass
                self.path_naive_greedy()
                # self.path_bfs()
                # self.path_dfs()
        

    def __check_collide(self):
        # 保证坦克不移出屏幕
        self.hero.hit_wall()
        for enemy in self.enemies:
            enemy.hit_wall_turn()

        # 子弹击中墙
        for wall in self.walls:
            # 我方英雄子弹击中墙
            for bullet in self.hero.bullets:
                if pygame.sprite.collide_rect(wall, bullet):
                    if wall.type == Settings.RED_WALL:
                        wall.kill()
                        bullet.kill()
                    #elif wall.type == Settings.BOSS_WALL:
                    #    self.game_still = False
                    elif wall.type == Settings.IRON_WALL:
                        bullet.kill()
            # 敌方英雄子弹击中墙
            for enemy in self.enemies:
                for bullet in enemy.bullets:
                    if pygame.sprite.collide_rect(wall, bullet):
                        if wall.type == Settings.RED_WALL:
                            wall.kill()
                            bullet.kill()
                        #elif wall.type == Settings.BOSS_WALL:
                        #    self.game_still = False
                        elif wall.type == Settings.IRON_WALL:
                            bullet.kill()

            # 我方坦克撞墙
            if pygame.sprite.collide_rect(self.hero, wall):
                # 不可穿越墙
                if wall.type == Settings.RED_WALL or wall.type == Settings.IRON_WALL:#or wall.type == Settings.BOSS_WALL:
                    self.hero.is_hit_wall = True
                    # 移出墙内
                    self.hero.move_out_wall(wall)

            # 敌方坦克撞墙
            for enemy in self.enemies:
                if pygame.sprite.collide_rect(wall, enemy):
                    if wall.type == Settings.RED_WALL or wall.type == Settings.IRON_WALL:# or wall.type == Settings.BOSS_WALL:
                        enemy.move_out_wall(wall)
                        enemy.random_turn()

        # 子弹击中、敌方坦克碰撞、敌我坦克碰撞
        pygame.sprite.groupcollide(self.hero.bullets, self.enemies, True, True)

        # 敌方子弹击中我方
        for enemy in self.enemies:
            for bullet in enemy.bullets:
                if pygame.sprite.collide_rect(bullet, self.hero):
                    bullet.kill()
                    self.hero.kill()

    def __update_sprites(self):
        # self.hero.update()
        if self.hero.is_moving:
            self.hero.update()
        self.walls.update()
        self.hero.bullets.update()
        self.enemies.update()
        for enemy in self.enemies:
            enemy.bullets.update()
            enemy.bullets.draw(self.screen)
        self.enemies.draw(self.screen)
        self.hero.bullets.draw(self.screen)
        self.screen.blit(self.hero.image, self.hero.rect)
        self.walls.draw(self.screen)

    def path_dfs(self):
        """
        找到距离self.hero最近的enemy，并使用深度优先搜索对hero做路径规划，使其一边射击，一边向enemy的方向走;
        如果没有找到合适的路径，随机生成一个
        """
        def is_valid(pos):
            x, y = pos
            if x < 0 or x >= Settings.SCREEN_RECT.width:
                return False
            if y < 0 or y >= Settings.SCREEN_RECT.height:
                return False
            return True

        # 计算两个物体之间的距离
        def distance(sprite1, sprite2):
            x1, y1 = sprite1.rect.center
            x2, y2 = sprite2.rect.center
            return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


        def dfs(start, end, max_depth=50):
            # 初始化栈和访问集合
            stack = [(start, 0)]
            visited = set()
            predecessors = {start: None}

            # 定义方向数组
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

            # 深度优先搜索
            while stack:
                current, depth = stack.pop()
                if ((current[0] - end[0]) ** 2 + (current[1] - end[1]) ** 2) ** 0.5<=Settings.HERO_SPEED*5:
                    # 找到目标，回溯路径
                    path = []
                    path.append(current)
                    #current = predecessors[current]
                    return path[::-1]

                if depth < max_depth:
                    for direction in directions:
                        next_pos = (current[0] + direction[0]*Settings.HERO_SPEED*5, current[1] + direction[1]*Settings.HERO_SPEED*5)
                        if next_pos not in visited:
                            # 检查下一个位置是否可行
                            if is_valid(next_pos):
                                stack.append((next_pos, depth + 1))
                                visited.add(next_pos)
                                predecessors[next_pos] = current

            # 没有找到路径，返回None
            return None


        if len(self.enemies):
            # self.hero.shot()
            nearest_enemy = min(self.enemies, key=lambda enemy: distance(self.hero, enemy))
            # 找到距离英雄最近的敌人
            nearest_enemy = min(self.enemies, key=lambda enemy: distance(self.hero, enemy))

            # 更新英雄的位置和方向
            path = dfs(self.hero.rect.center, nearest_enemy.rect.center)
            #print(path)

        if path:
            next_pos = path[0]
            if next_pos[0] < self.hero.rect.centerx:
                self.hero.direction = Settings.LEFT
            elif next_pos[0] > self.hero.rect.centerx:
                self.hero.direction = Settings.RIGHT
            elif next_pos[1] < self.hero.rect.centery:
                self.hero.direction = Settings.UP
            elif next_pos[1] > self.hero.rect.centery:
                self.hero.direction = Settings.DOWN

        # 英雄射击

            self.hero.is_moving = True
            self.hero.is_hit_wall = False
            self.hero.update()
        else:
            directions = [i for i in range(4)]
            self.hero.direction = directions[random.randint(0, 2)]
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
            self.hero.update()
        self.hero.shot()


    def path_bfs(self):
        """
        找到距离self.hero最近的enemy，并使用广度优先搜索对hero做路径规划，使其一边射击，一边向enemy的方向走;
        如果没有找到合适的路径，随机生成一个
        """
        def is_valid(pos):
            x, y = pos
            if x < 0 or x >= Settings.SCREEN_RECT.width:
                return False
            if y < 0 or y >= Settings.SCREEN_RECT.height:
                return False
            return True

        # 计算两个物体之间的距离
        def distance(sprite1, sprite2):
            x1, y1 = sprite1.rect.center
            x2, y2 = sprite2.rect.center
            return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        # 使用广度优先搜索算法对英雄进行路径规划
        def bfs(start, end):
            # 初始化队列和访问集合
            queue = [start]
            visited = set()
            predecessors = {start: None}

            # 定义方向数组
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

            # 广度优先搜索
            while queue:
                current = queue.pop(0)
                # print(((current[0] - end[0]) ** 2 + (current[1] - end[1]) ** 2) ** 0.5)
                if ((current[0] - end[0]) ** 2 + (current[1] - end[1]) ** 2) ** 0.5<=Settings.HERO_SPEED*5:
                    # 找到目标，回溯路径
                    path = []
                    # while current:
                    path.append(current)
                    # current = predecessors[current]
                    return path[::-1]

                for direction in directions:
                    next_pos = (current[0] + direction[0]*Settings.HERO_SPEED*5, current[1] + direction[1]*Settings.HERO_SPEED*5)
                    if next_pos not in visited:
                        # 检查下一个位置是否可行
                        if is_valid(next_pos):
                            queue.append(next_pos)
                            visited.add(next_pos)
                            predecessors[next_pos] = current

            # 没有找到路径，返回None
            return None

        # 找到距离英雄最近的敌人
        path = None
        if len(self.enemies):
            # self.hero.shot()
            nearest_enemy = min(self.enemies, key=lambda enemy: distance(self.hero, enemy))
            # 更新英雄的位置和方向
            path = bfs(self.hero.rect.center, nearest_enemy.rect.center)
        # print(path)

        if path:
            next_pos = path[0]
            if next_pos[0] < self.hero.rect.centerx:
                self.hero.direction = Settings.LEFT
            elif next_pos[0] > self.hero.rect.centerx:
                self.hero.direction = Settings.RIGHT
            elif next_pos[1] < self.hero.rect.centery:
                self.hero.direction = Settings.UP
            elif next_pos[1] > self.hero.rect.centery:
                self.hero.direction = Settings.DOWN

        # 英雄射击

            self.hero.is_moving = True
            self.hero.is_hit_wall = False
            self.hero.update()

    def path_naive_greedy(self):
        """
        找到距离self.hero最近的enemy，计算和目标之间的相对位置，根据相对位置确定下一个前进方向
        """
        def distance(sprite1, sprite2):
            x1, y1 = sprite1.rect.center
            x2, y2 = sprite2.rect.center
            return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        # 找到距离英雄最近的敌人
        if len(self.enemies):
            # self.hero.shot()
            nearest_enemy = min(self.enemies, key=lambda enemy: distance(self.hero, enemy))

            # 计算英雄和目标之间的相对位置
            dx = nearest_enemy.rect.centerx - self.hero.rect.centerx
            dy = nearest_enemy.rect.centery - self.hero.rect.centery

            # 根据相对位置确定下一个前进方向
            if abs(dx) > abs(dy):
                if dx < 0:
                    next_direction = Settings.LEFT
                else:
                    next_direction = Settings.RIGHT
            else:
                if dy < 0:
                    next_direction = Settings.UP
                else:
                    next_direction = Settings.DOWN

            # 更新英雄的方向
            self.hero.direction = next_direction
            # print(next_direction,self.hero.rect.center)
            self.hero.is_moving = True
            # self.hero.is_hit_wall = False
            self.hero.update()



    def run_game(self):
        self.__init_game()
        self.__create_sprite()
        start_time = time.time()
        time0_1 = time.time()
        while True and self.hero.is_alive and self.game_still:
            spentTime = time.time() - start_time
            self.hero.shot() # ??? hero shot only after last bullet killed ???
            self.screen.fill(Settings.SCREEN_COLOR)
            # 1、设置刷新帧率
            self.clock.tick(Settings.FPS)
            # 2、事件监听
            
            # Our AI hero
            # if pygame.time.get_ticks()% 1000 != 0:
            self.__AI_handler()
            
            # Player control hero by keyboard
            # self.__event_handler()
            
            # 3、碰撞监测
            self.__check_collide()
            # 4、更新/绘制精灵/经理组
            self.__update_sprites()
            # 5、更新显示
            
            # Reward value
            score = 100*(1 - len(self.enemies)) - round(spentTime,1)
            
            font = pygame.font.SysFont('宋体', 20, True)
            score_surface1 = font.render("Reward:" + str(score), True, (255, 255, 255))
            # score_surface2 = font.render("Hp:" + str(self.hero.life), True, (255, 255, 255))
            score_surface2 = font.render("Time:" + str(round(Settings.TIME_LIMIT - spentTime,1)), True, (255, 255, 255))
            score_rect1 = score_surface1.get_rect()
            score_rect2 = score_surface1.get_rect()
            score_rect1.right = 19*Settings.BOX_SIZE - 10
            score_rect2.right = 19 * Settings.BOX_SIZE - 10
            score_rect1.top = 10
            score_rect2.top = 30
            self.screen.blit(score_surface1, score_rect1)
            self.screen.blit(score_surface2, score_rect2)
            pygame.display.update()
            self.hero.is_moving = False
            
            if spentTime > Settings.TIME_LIMIT or len(self.enemies) == 0:

                print("击杀数：{}".format(score))
                print("剩余血量：{}".format(self.hero.life))
                pygame.quit()
                break
        
        score = 100*(1 - len(self.enemies)) - round(spentTime,1)
        self.__game_over(score)

    @staticmethod
    def __game_over(score):
        pygame.init()

        # 创建总结数据窗口
        summary_window_width = 960
        summary_window_height = 540
        summary_window = pygame.display.set_mode((summary_window_width, summary_window_height))
        pygame.display.set_caption("Summary Data")

        # 渲染总结数据文本
        summary_data_font = pygame.font.Font(None, 24)
        summary_data_text = ("Score: {}".format(score))
        summary_data_render = summary_data_font.render(summary_data_text, True, (255, 255, 255))

        # 在总结数据窗口中居中绘制文本
        summary_data_x = (summary_window_width - summary_data_render.get_width()) // 2
        summary_data_y = (summary_window_height - summary_data_render.get_height()) // 2
        summary_window.blit(summary_data_render, (summary_data_x, summary_data_y))

        # 更新总结数据窗口并等待关闭事件
        pygame.display.flip()
        
        
        # pygame.event.set_grab(True)
        # pygame.mouse.set_visible(False)

        while True:
            # Event handling
            
            # pygame.event.set_grab(True)
            # pygame.mouse.set_visible(False)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

        exit()
