import tkinter as tk
import random

ROW = 25
COL = 25
TILE_SIZE = 25
WINDOWS_WIDTH = COL * TILE_SIZE
WINDOWS_HEIGHT = ROW * TILE_SIZE

INITIAL_SNAKE_X = 5 * TILE_SIZE
INITIAL_SNAKE_Y = 5 * TILE_SIZE
INITIAL_FOOD_X = 10 * TILE_SIZE
INITIAL_FOOD_Y = 10 * TILE_SIZE
GAME_SPEED = 100

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SnakeGame:
    def __init__(self):
        self.window = self.setup_window()
        self.canvas = self.setup_canvas()
        self.snake = Tile(INITIAL_SNAKE_X, INITIAL_SNAKE_Y)
        self.food = self.generate_food()
        self.snake_body = []
        self.velocity_x = 0
        self.velocity_y = 0
        self.game_over = False
        self.score = 0
        self.game_loop_id = None

    DIRECTION_MAP = {
        "Up": (0, -1),
        "Down": (0, 1),
        "Left": (-1, 0),
        "Right": (1, 0)
    }

    def setup_window(self):
        window = tk.Tk()
        window.title("Snake Game")
        window.resizable(False, False)
        self.center_window(window)
        return window

    def setup_canvas(self):
        canvas = tk.Canvas(self.window, width=WINDOWS_WIDTH, height=WINDOWS_HEIGHT, 
                            bg="black", borderwidth=0, highlightthickness=0)
        canvas.pack()
        self.window.update()
        return canvas

    def center_window(self, window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width/2) - (WINDOWS_WIDTH/2))
        y = int((screen_height/2) - (WINDOWS_HEIGHT/2))
        window.geometry(f"{WINDOWS_WIDTH}x{WINDOWS_HEIGHT}+{x}+{y}")

    def generate_food(self):
        while True:
            food = Tile(
                random.randint(0, COL-1) * TILE_SIZE,
                random.randint(0, ROW-1) * TILE_SIZE
            )
            if food.x != self.snake.x or food.y != self.snake.y:
                return food

    def change_direction(self, event):
        if self.game_over:
            return
        
        new_direction = self.DIRECTION_MAP.get(event.keysym)
        if new_direction:
            opposite_current = (-self.velocity_x, -self.velocity_y)
            if new_direction != opposite_current:
                self.velocity_x, self.velocity_y = new_direction

    def check_collisions(self):
        if (self.snake.x < 0 or self.snake.x >= WINDOWS_WIDTH or 
            self.snake.y < 0 or self.snake.y >= WINDOWS_HEIGHT):
            return True
        
        return any(self.snake.x == tile.x and self.snake.y == tile.y 
                   for tile in self.snake_body)

    def move_snake(self):
        if self.game_over:
            return
        
        new_head_x = self.snake.x + self.velocity_x * TILE_SIZE
        new_head_y = self.snake.y + self.velocity_y * TILE_SIZE
        
        if (new_head_x < 0 or new_head_x >= WINDOWS_WIDTH or 
            new_head_y < 0 or new_head_y >= WINDOWS_HEIGHT):
            self.game_over = True
            return
        
        if any(new_head_x == tile.x and new_head_y == tile.y for tile in self.snake_body):
            self.game_over = True
            return
        
        if new_head_x == self.food.x and new_head_y == self.food.y:
            self.snake_body.append(Tile(self.snake.x, self.snake.y))
            self.food = self.generate_food()
            self.score += 1
        
        if self.snake_body:
            self.snake_body = [Tile(self.snake.x, self.snake.y)] + self.snake_body[:-1]
        
        self.snake.x = new_head_x
        self.snake.y = new_head_y

    def draw_food(self):
        self.canvas.create_rectangle(
            self.food.x, self.food.y, 
            self.food.x + TILE_SIZE, self.food.y + TILE_SIZE, 
            fill="red", width=0
        )

    def draw_snake(self):
        self.canvas.create_rectangle(
            self.snake.x, self.snake.y, 
            self.snake.x + TILE_SIZE, self.snake.y + TILE_SIZE, 
            fill="lime green", width=0
        )
        for tile in self.snake_body:
            self.canvas.create_rectangle(
                tile.x, tile.y, 
                tile.x + TILE_SIZE, tile.y + TILE_SIZE, 
                fill="lime green", width=0
            )

    def draw_game_over(self):
        self.draw_score()
        self.canvas.create_text(
            WINDOWS_WIDTH / 2, WINDOWS_HEIGHT / 2, 
            text="Game Over", 
            font=("Arial", 20), fill="white"
        )
        self.canvas.create_text(
            WINDOWS_WIDTH / 2, WINDOWS_HEIGHT / 2 + 40, 
            text="Press 'R' to restart", 
            font=("Arial", 16), fill="white"
        )

    def draw_score(self):
        self.canvas.create_text(
            10, 10, anchor="nw", text=f"Score: {self.score}", 
            font=("Arial", 16), fill="white"
        )

    def draw_game(self):
        self.canvas.delete("all")
        self.draw_food()
        self.draw_snake()
        
        if self.game_over:
            self.draw_game_over()
        elif self.velocity_x == 0 and self.velocity_y == 0:
            self.draw_start_message()
        else:
            self.draw_score()
        
        if not self.game_over:
            self.move_snake()
            self.game_loop_id = self.window.after(GAME_SPEED, self.draw_game)

    def draw_start_message(self):
        self.canvas.create_text(
            WINDOWS_WIDTH / 2, WINDOWS_HEIGHT / 2,
            text="Press an arrow key to start",
            font=("Arial", 16), fill="white"
        )

    def restart_game(self):
        if self.game_loop_id:
            self.window.after_cancel(self.game_loop_id)
            self.game_loop_id = None
        
        self.snake = Tile(INITIAL_SNAKE_X, INITIAL_SNAKE_Y)
        self.snake_body = []
        self.food = self.generate_food()
        self.game_over = False
        self.score = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.draw_game()

    def run(self):
        self.draw_game()
        self.window.bind("<KeyPress>", self.change_direction)
        self.window.bind("<KeyPress-r>", lambda event: self.restart_game())
        self.window.mainloop()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()