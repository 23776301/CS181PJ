import tkinter as tk
import random

# 定义地图和障碍物
MAP_WIDTH = 500
MAP_HEIGHT = 500
OBSTACLES = [(100, 99), (200, 200), (300, 300), (400, 400)]
path = []
for i in range(100,300):
    OBSTACLES.append((100,i))
    OBSTACLES.append((i,100))

'''
targetaction = [(-1,-1),(-1,0),(0,0),(1,0),(0,-1),(0,1),(1,-1),(1,1)]
for i in range(20):
    path.append(targetaction[random.randint(0,7)])
print(path)
'''
# target 沿固定路径移动
path = [(0, 0), (0, -1), (0, 1), (0, 0), (1, 1), (-1, 0), (1, -1), (0, 1), (1, 1), (0, 0), (0, 0), (1, 1), (-1, -1), (0, -1), (1, 1), (0, -1), (1, 0), (-1, 0), (1, 0), (-1, 0), (0, 0), (0, 1), (1, 0), (-1, 0), (-1, -1), (1, 1), (1, 1), (-1, -1), (0, -1), (1, 0), (-1, 0), (-1, 0), (1, 1), (1, 0), (-1, -1), (0, -1), (0, -1), (1, 1), (-1, 0), (0, -1), (1, -1), (-1, 0), (1, -1), (-1, 0), (1, 0), (1, 0), (1, 1), (1, 1), (0, 1), (1, 0)]


# 定义智能体和目标
AGENT_RADIUS = 10
AGENT_COLOR = 'blue'
TARGET_RADIUS = 10
TARGET_COLOR = 'red'

class Agent:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = AGENT_RADIUS
        self.color = AGENT_COLOR
        self.score = score

    def move(self):
        self.score -= 1
        self.x += self.vx
        self.y += self.vy

    def draw(self, canvas):
        canvas.create_oval(self.x - self.radius, self.y - self.radius,
                           self.x + self.radius, self.y + self.radius,
                           fill=self.color)

class Target:
    def __init__(self, x, y, path):
        self.x = x
        self.y = y
        self.radius = TARGET_RADIUS
        self.color = TARGET_COLOR
        self.step = 0
        self.path = path


    def draw(self, canvas):
        canvas.create_oval(self.x - self.radius, self.y - self.radius,
                           self.x + self.radius, self.y + self.radius,
                           fill=self.color)
    def move(self, path):
        if self.step > 5000 or self.x > 490 or self.x < 10 or self.y < 10 or self.y > 490 :
            return
        self.x += path[self.step % 50][0]
        self.y += path[self.step % 50][1]
        self.step += 1

# 实现智能体的移动策略
def greedy_1(agent, target):
    #撞墙后通过随机动作绕路
    dx = target.x - agent.x
    dy = target.y - agent.y
    dist = (dx ** 2 + dy ** 2) ** 0.5
    if dist > 10:
        agent.vx = dx / dist
        agent.vy = dy / dist
    else:
        agent.score += 10000
        agent.vx = 0
        agent.vy = 0
        return agent.score

    # 检查是否碰到障碍物
    for obstacle in OBSTACLES:
        if (agent.x - obstacle[0]) ** 2 + (agent.y - obstacle[1]) ** 2 < (AGENT_RADIUS + 5) ** 2:
            agent.vx = -agent.vx
            agent.vy = -agent.vy
            if agent.x >= obstacle[0] and agent.y >= obstacle[1]: #障碍在左上角
                actions = [(0, -1), (1, 0)]
                action = actions[random.randint(0,1)]
                agent.vx = action[0]
                agent.vy = action[1]
            elif agent.x <= obstacle[0] and agent.y >= obstacle[1]: #障碍在右上角
                actions = [(0,-1), (-1,0)]
                action = actions[random.randint(0,1)]
                agent.vx = action[0]
                agent.vy = action[1]
            elif agent.x >= obstacle[0] and agent.y <= obstacle[1]: #障碍在左下角
                actions = [(0,1), (1,0)]
                action = actions[random.randint(0,1)]
                agent.vx = action[0]
                agent.vy = action[1]
            elif agent.x <= obstacle[0] and agent.y <= obstacle[1]: #障碍在右下角
                actions = [(0,-1), (-1,0)]
                action = actions[random.randint(0,1)]
                agent.vx = action[0]
                agent.vy = action[1]

            break

    agent.move()
    target.move(path)
    return agent.score




# 实现智能体和目标的交互
def update(agent, target):#, canvas):
    result = greedy_1(agent, target)
    #canvas.delete('all')
    #for obstacle in OBSTACLES:
    #    canvas.create_rectangle(obstacle[0] - 5, obstacle[1] - 5,
    #                            obstacle[0] + 5, obstacle[1] + 5,
    #                            fill='gray')
    #agent.draw(canvas)
    #target.draw(canvas)
    return result

# 用tkinter展示效果
def main():
    root = tk.Tk()
    #root.title('Agent Tracking Target')
    #canvas = tk.Canvas(root, width=MAP_WIDTH, height=MAP_HEIGHT)
    #canvas.pack()

    # 初始化智能体和目标
    agent = Agent(MAP_WIDTH // 2, MAP_HEIGHT // 2, 0)
    #target = Target(random.randint(0, MAP_WIDTH), random.randint(0, MAP_HEIGHT))
    target = Target(50, 50, path)

    # 更新画面
    def update_canvas():
        result = update(agent, target)
        if result > 0:
           print(result)
           print('step = ' + str(10000 - result))
           root.quit()
        root.after(10, update_canvas)
        return result

    result = update_canvas()
    root.mainloop()


        
if __name__ == '__main__':
    main()
