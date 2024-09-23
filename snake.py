import tkinter
import random

ROW = 25
COL = 25
TILE_SIZE = 25
WINDOWS_WIDTH = COL * TILE_SIZE
WINDOWS_HEIGHT = ROW * TILE_SIZE

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SnakeGame:
    def __init__(self):
        self.window = self.setup_window()
        self.canvas = self.setup_canvas()
        self.snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
        self.food = self.generate_food()
        self.snake_body = []
        self.velocity_x = 0
        self.velocity_y = 0
        self.game_over = False
        self.score = 0
        self.game_loop_id = None

    def setup_window(self):
        window = tkinter.Tk()
        window.title("Snake Game")
        window.resizable(False, False)
        self.center_window(window)
        return window

    def setup_canvas(self):
        canvas = tkinter.Canvas(self.window, width=WINDOWS_WIDTH, height=WINDOWS_HEIGHT, 
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
        food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
        while food.x == self.snake.x and food.y == self.snake.y:
            food.x = random.randint(0, COL-1) * TILE_SIZE
            food.y = random.randint(0, ROW-1) * TILE_SIZE
        return food

    def change_direction(self, event):
        if self.game_over:
            return
        
        if event.keysym == "Up" and self.velocity_y != 1:
            self.velocity_x, self.velocity_y = 0, -1
        elif event.keysym == "Down" and self.velocity_y != -1:
            self.velocity_x, self.velocity_y = 0, 1
        elif event.keysym == "Left" and self.velocity_x != 1:
            self.velocity_x, self.velocity_y = -1, 0
        elif event.keysym == "Right" and self.velocity_x != -1:
            self.velocity_x, self.velocity_y = 1, 0

    def move_snake(self):
        if self.game_over:
            return
        
        # Check for collisions
        if (self.snake.x < 0 or self.snake.x >= WINDOWS_WIDTH or 
            self.snake.y < 0 or self.snake.y >= WINDOWS_HEIGHT):
            self.game_over = True
            return
        
        for tile in self.snake_body:
            if self.snake.x == tile.x and self.snake.y == tile.y:
                self.game_over = True
                return
        
        # Check for collision with food
        if self.snake.x == self.food.x and self.snake.y == self.food.y:
            self.snake_body.append(Tile(self.snake.x, self.snake.y))
            self.food = self.generate_food()
            self.score += 1
        
        # Update the snake's body
        for i in range(len(self.snake_body)-1, -1, -1):
            tile = self.snake_body[i]
            if i == 0:
                tile.x, tile.y = self.snake.x, self.snake.y
            else:
                prev_tile = self.snake_body[i-1]
                tile.x, tile.y = prev_tile.x, prev_tile.y
        
        self.snake.x += self.velocity_x * TILE_SIZE
        self.snake.y += self.velocity_y * TILE_SIZE

    def draw_game(self):
        self.move_snake()
        
        self.canvas.delete("all")
        self.canvas.create_rectangle(self.food.x, self.food.y, 
                                     self.food.x+TILE_SIZE, self.food.y+TILE_SIZE, 
                                     fill="red", width=0)
        self.canvas.create_rectangle(self.snake.x, self.snake.y, 
                                     self.snake.x+TILE_SIZE, self.snake.y+TILE_SIZE, 
                                     fill="lime green", width=0)
        
        for tile in self.snake_body:
            self.canvas.create_rectangle(tile.x, tile.y, 
                                         tile.x+TILE_SIZE, tile.y+TILE_SIZE, 
                                         fill="lime green", width=0)
        
        if self.game_over:
            self.canvas.create_text(WINDOWS_WIDTH/2, WINDOWS_HEIGHT/2, 
                                    text=f"Game Over: {self.score}", 
                                    font=("Arial", 20), fill="white")
            self.canvas.create_text(WINDOWS_WIDTH/2, WINDOWS_HEIGHT/2 + 40, 
                                    text="Press 'R' to restart", 
                                    font=("Arial", 16), fill="white")
        else:
            self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}", 
                                    font=("Arial", 16), fill="white")
            
        if not self.game_over:
            self.game_loop_id = self.window.after(100, self.draw_game)

    def restart_game(self):
        if self.game_loop_id:
            self.window.after_cancel(self.game_loop_id)
            self.game_loop_id = None
        
        self.snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
        self.snake_body = []
        self.food = self.generate_food()
        self.game_over = False
        self.score = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.draw_game()

    def run(self):
        self.draw_game()
        self.window.bind("<KeyPress-r>", lambda event: self.restart_game())
        self.window.bind("<KeyRelease>", self.change_direction)
        self.window.mainloop()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()