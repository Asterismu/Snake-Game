import tkinter as tk
import random

class Menu(tk.Tk):
    def __init__(self, game):
        super().__init__()

        self.title("Snake Game Menu")
        self.geometry("200x200")
        self.game = game

        new_game_button = tk.Button(self, text="新游戏", command=self.new_game)
        new_game_button.pack(pady=20)

        quit_button = tk.Button(self, text="退出游戏", command=self.quit_game)
        quit_button.pack(pady=20)

    def new_game(self):
        self.game.new_game()
        self.game.deiconify()  # Show the game window
        self.withdraw()  # Hide the menu window

    def quit_game(self):
        self.game.quit()
        self.quit()

class Game(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Snake Game")
        self.geometry("600x600")
        self.snake = [(10, 10), (10, 20), (10, 30)]
        self.food = None
        self.paused = False

        self.canvas = tk.Canvas(self, width=600, height=600)
        self.canvas.pack()

        self.bind("<Key>", self.change_direction)
        self.bind("<Key-x>", self.pause_game)

        self.withdraw()  # Hide the game window until a new game starts

        self.menu = Menu(self)
        self.menu.mainloop()

    def new_game(self):
        self.canvas.delete("all")
        self.snake = [(10, 10), (10, 20), (10, 30)]
        self.food = None
        self.direction = "Right"
        self.game_over = False
        self.score = 0
        self.paused = False
        self.move_snake()
        self.create_food()

    def pause_game(self, event):
        self.paused = not self.paused

    def change_direction(self, event):
        if event.keysym == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif event.keysym == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif event.keysym == "Right" and self.direction != "Left":
            self.direction = "Right"

    def create_food(self):
        while self.food is None:
            food = (random.randint(1, 59) * 10, random.randint(1, 59) * 10)
            if food not in self.snake:
                self.food = food

        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0] + 10, self.food[1] + 10, fill="red")

    def move_snake(self):
        if not self.game_over and not self.paused:
            head_x, head_y = self.snake[0]
            if self.direction == "Left":
                new_head = (head_x - 10, head_y)
            elif self.direction == "Right":
                new_head = (head_x + 10, head_y)
            elif self.direction == "Up":
                new_head = (head_x, head_y - 10)
            else:  # self.direction == "Down"
                new_head = (head_x, head_y + 10)

            if new_head in self.snake or new_head[0] < 0 or new_head[0] >= 600 or new_head[1] < 0 or new_head[1] >= 600:
                self.game_over = True
                self.menu.deiconify()  # Show the menu window
                self.withdraw()  # Hide the game window
                return

            self.snake = [new_head] + self.snake

            if new_head == self.food:
                self.score += 10
                self.food = None
                self.canvas.create_oval(new_head[0], new_head[1], new_head[0] + 10, new_head[1] + 10, fill="yellow")
                self.after(100, self.canvas.delete, "all")
            else:
                self.snake.pop()

            self.canvas.delete("all")
            for x, y in self.snake:
                self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="green")

            self.create_food()
            self.canvas.create_text(50, 10, fill="darkblue", font="Times 20 italic bold",
                                    text=f"得分: {self.score}")

        self.after(100, self.move_snake)

if __name__ == "__main__":
    game = Game()
    game.mainloop()