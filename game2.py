import tkinter as tk
from tkinter import messagebox


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_wall = False

    def draw(self, canvas, cell_size):
        x1 = self.col * cell_size
        y1 = self.row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size

        if self.is_wall:
            canvas.create_rectangle(x1, y1, x2, y2, fill="black")
        else:
            canvas.create_rectangle(x1, y1, x2, y2, fill="white")


class Agent:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.direction = None

    def move(self, direction, game_space):
        next_row, next_col = self.get_next_position(direction)
        if self.is_valid_move(next_row, next_col, game_space):
            self.row = next_row
            self.col = next_col

    def get_next_position(self, direction):
        if direction == "up":
            return self.row - 1, self.col
        elif direction == "down":
            return self.row + 1, self.col
        elif direction == "left":
            return self.row, self.col - 1
        elif direction == "right":
            return self.row, self.col + 1

    def is_valid_move(self, row, col, game_space):
        if row < 0 or row >= len(game_space) or col < 0 or col >= len(game_space[0]):
            return False
        if game_space[row][col] != 0:
            return False
        return True

    def fire_bullet(self):
        return Bullet(self.row, self.col, self.direction, 1, "agent")

    def draw(self, canvas, cell_size):
        x1 = self.col * cell_size
        y1 = self.row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size
        canvas.create_oval(x1, y1, x2, y2, fill="red")


class Target:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.direction = None

    def move(self, direction, game_space):
        next_row, next_col = self.get_next_position(direction)
        if self.is_valid_move(next_row, next_col, game_space):
            self.row = next_row
            self.col = next_col

    def get_next_position(self, direction):
        if direction == "up":
            return self.row - 1, self.col
        elif direction == "down":
            return self.row + 1, self.col
        elif direction == "left":
            return self.row, self.col - 1
        elif direction == "right":
            return self.row, self.col + 1

    def is_valid_move(self, row, col, game_space):
        if row < 0 or row >= len(game_space) or col < 0 or col >= len(game_space[0]):
            return False
        if game_space[row][col] != 0:
            return False
        return True

    def fire_bullet(self):
        return Bullet(self.row, self.col, self.direction, 1, "target")

    def draw(self, canvas, cell_size):
        x1 = self.col * cell_size
        y1 = self.row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size
        canvas.create_oval(x1, y1, x2, y2, fill="blue")


class Bullet:
    def __init__(self, row, col, direction, speed, owner):
        self.row = row
        self.col = col
        self.direction = direction
        self.speed = speed
        self.owner = owner

    def move(self, game_space):
        next_row, next_col = self.get_next_position()
        if self.is_valid_move(next_row, next_col, game_space):
            self.row = next_row
            self.col = next_col

    def get_next_position(self):
        if self.direction == "up":
            return self.row - self.speed, self.col
        elif self.direction == "down":
            return self.row + self.speed, self.col
        elif self.direction == "left":
            return self.row, self.col - self.speed
        elif self.direction == "right":
            return self.row, self.col + self.speed

    def is_valid_move(self, row, col, game_space):
        if row < 0 or row >= len(game_space) or col < 0 or col >= len(game_space[0]):
            return False
        if game_space[row][col] != 0:
            return False
        return True

    def hit_opponent(self, opponent):
        return self.row == opponent.row and self.col == opponent.col

    def draw(self, canvas, cell_size):
        x1 = self.col * cell_size
        y1 = self.row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size
        if self.owner == "agent":
            canvas.create_rectangle(x1, y1, x2, y2, fill="red")
        elif self.owner == "target":
            canvas.create_rectangle(x1, y1, x2, y2, fill="blue")


class Game:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.cell_size = 30
        self.space = [[0] * grid_size[1] for _ in range(grid_size[0])]
        self.window = tk.Tk()
        self.canvas = tk.Canvas(
            self.window,
            width=self.grid_size[1] * self.cell_size,
            height=self.grid_size[0] * self.cell_size,
        )
        self.canvas.pack()
        self.agent = Agent(1, 1)
        self.target = Target(grid_size[0] - 2, grid_size[1] - 2)
        self.agent_bullet = None
        self.target_bullet = None
        self.is_game_over = False

        self.window.bind("<Up>", self.key_press)
        self.window.bind("<Down>", self.key_press)
        self.window.bind("<Left>", self.key_press)
        self.window.bind("<Right>", self.key_press)
        self.window.bind("<space>", self.key_press)

    def key_press(self, event):
        if not self.is_game_over:
            if event.keysym == "Up":
                self.agent.direction = "up"
            elif event.keysym == "Down":
                self.agent.direction = "down"
            elif event.keysym == "Left":
                self.agent.direction = "left"
            elif event.keysym == "Right":
                self.agent.direction = "right"
            elif event.keysym == "space" and self.agent_bullet is None:
                self.agent_bullet = self.agent.fire_bullet()

    def update(self):
        if not self.is_game_over:
            if self.agent.direction:
                self.agent.move(self.agent.direction, self.space)
            if self.target.direction:
                self.target.move(self.target.direction, self.space)

            if self.agent_bullet:
                self.agent_bullet.move(self.space)
                if self.agent_bullet.hit_opponent(self.target):
                    self.is_game_over = True
                    messagebox.showinfo("Game Over", "Agent wins!")
                elif self.agent_bullet.is_valid_move(
                    self.agent_bullet.row, self.agent_bullet.col, self.space
                ):
                    self.space[self.agent_bullet.row][self.agent_bullet.col] = 4
                else:
                    self.agent_bullet = None

            if self.target_bullet:
                self.target_bullet.move(self.space)
                if self.target_bullet.hit_opponent(self.agent):
                    self.is_game_over = True
                    messagebox.showinfo("Game Over", "Target wins!")
                elif self.target_bullet.is_valid_move(
                    self.target_bullet.row, self.target_bullet.col, self.space
                ):
                    self.space[self.target_bullet.row][self.target_bullet.col] = 5
                else:
                    self.target_bullet = None

            self.space[self.agent.row][self.agent.col] = 1
            self.space[self.target.row][self.target.col] = 2

            self.draw()

    def draw(self):
        self.canvas.delete(tk.ALL)

        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                cell = Cell(row, col)
                cell.is_wall = self.space[row][col] == 3
                cell.draw(self.canvas, self.cell_size)

        self.agent.draw(self.canvas, self.cell_size)
        self.target.draw(self.canvas, self.cell_size)

        if self.agent_bullet:
            self.agent_bullet.draw(self.canvas, self.cell_size)
        if self.target_bullet:
            self.target_bullet.draw(self.canvas, self.cell_size)

    def start(self):
        self.space[self.agent.row][self.agent.col] = 1
        self.space[self.target.row][self.target.col] = 2

        self.draw()
        self.window.after(100, self.update)
        self.window.mainloop()


game = Game((10, 10))
game.start()
