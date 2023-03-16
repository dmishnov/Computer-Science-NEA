import tkinter as tk
import random

GAME_WIDTH = 10
GAME_HEIGHT = 22

BLOCK_SIZE = 30
COLOURS = [
    "#000000",  # black
    "#f66d9b",  # pink
    "#9561e2",  # purple
    "#6574cd",  # light blue
    "#3490dc",  # blue
    "#4dc0b5",  # blue-green
    "#38c172",  # green
    "#ffed4a",  # yellow
    "#f6993f",  # orange
    "#e3342f",  # red
]

TETROMINOS = [
    [
        [(0, 0), (0, 1), (1, 0), (1, 1)],  # O
        [(0, 0), (0, 1), (1, 0), (1, 1)],  # O
        [(0, 0), (0, 1), (1, 0), (1, 1)],  # O
        [(0, 0), (0, 1), (1, 0), (1, 1)],  # O
    ],
    [
        [(0, -1), (0, 0), (0, 1), (1, 1)],  # L
        [(0, 0), (-1, 1), (-1, 0), (1, 0)],  # L first turn
        [(0, 0), (-1, -1), (0, -1), (0, 1)],  # L second turn
        [(0, 0), (-1, 0), (1, 0), (1, -1)],  # L third turn
    ],
    [
        [(-1, 1), (0, 1), (0, 0), (0, -1)],  # J
        [(-1, -1), (-1, 0), (0, 0), (1, 0)],  # J first turn
        [(0, -1), (1, -1), (0, 0), (0, 1)],  # J second turn
        [(-1, 0), (0, 0), (1, 0), (1, 1)],  # J third turn
    ],
    [
        [(-1, 0), (0, 0), (1, 0), (0, 1)],  # T
        [(0, -1), (0, 0), (0, 1), (-1, 0)],  # T first turn
        [(-1, 0), (0, 0), (0, -1), (1, 0)],  # T second turn
        [(0, -1), (0, 0), (0, 1), (1, 0)],  # T third turn
    ],
    [
        [(0, 0), (0, -1), (0, 1), (0, 2)],  # I
        [(0, 0), (-1, 0), (1, 0), (2, 0)],  # I first turn
        [(0, 0), (0, -1), (0, 1), (0, 2)],  # I second turn
        [(0, 0), (-1, 0), (1, 0), (2, 0)],  # I third turn
    ],
    [
        [(0, 0), (0, -1), (-1, 0), (1, -1)],  # S
        [(-1, -1), (-1, 0), (0, 0), (0, 1)],  # S first turn
        [(0, 0), (0, -1), (-1, 0), (1, -1)],  # S second turn
        [(-1, -1), (-1, 0), (0, 0), (0, 1)],  # S third turn
    ],
    [
        [(-1, -1), (0, -1), (0, 0), (1, 0)],  # Z
        [(0, 0), (-1, 0), (0, -1), (-1, 1)],  # Z first turn
        [(-1, -1), (0, -1), (0, 0), (1, 0)],  # Z second turn
        [(0, 0), (-1, 0), (0, -1), (-1, 1)],  # Z third turn
    ],
]


class Game:
    def __init__(self):
        self.grid = [[0 for x in range(GAME_WIDTH)] for y in range(GAME_HEIGHT)]
        self.make_tetromino()
        self.total_score = 0
        self.total_lines_eliminated = 0
        self.score_multiplier = [0, 40, 100, 300, 1200]

    def make_tetromino(self):
        self.piece_colour = random.randint(1, len(COLOURS) - 1)
        self.current_coord = [GAME_WIDTH // 2, 0]
        self.tetromino_id = random.randint(0, len(TETROMINOS) - 1)
        self.rotation_id = 0
        self.tetromino = TETROMINOS[self.tetromino_id][self.rotation_id]

    def get_tetromino_coords(self):
        return [
            (x + self.current_coord[0], y + self.current_coord[1])
            for x, y in self.tetromino
        ]

    def set_colour(self):
        for x, y in self.get_tetromino_coords():
            self.grid[y][x] = self.piece_colour
        new_grid = [row for row in self.grid if any(tile == 0 for tile in row)]
        lines_eliminated = len(self.grid) - len(new_grid)
        score = self.score_multiplier[lines_eliminated]
        self.total_score += score
        self.total_lines_eliminated += lines_eliminated
        self.grid = [[0] * GAME_WIDTH for x in range(lines_eliminated)] + new_grid
        self.make_tetromino()

    def is_block_free(self, x, y):
        if x >= GAME_WIDTH or x < 0:
            return False
        if y >= GAME_HEIGHT or y < 0:
            return False
        if self.grid[y][x] != 0:
            return False

        return True

    def get_colour(self, x, y):
        if (x, y) in self.get_tetromino_coords():
            return self.piece_colour
        else:
            return self.grid[y][x]

    def move_tetromino(self, dx, dy):
        if all(
            self.is_block_free(x + dx, y + dy) for x, y in self.get_tetromino_coords()
        ):
            self.current_coord = [
                self.current_coord[0] + dx,
                self.current_coord[1] + dy,
            ]
            return True
        elif dx == 0 and dy == 1:
            self.set_colour()
            return False

    def rotate(self):
        self.rotation_id = (self.rotation_id + 1) % 4
        self.tetromino = TETROMINOS[self.tetromino_id][self.rotation_id]


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.game = Game()
        self.pack()
        self.draw_game()
        self.update_game()
        self.clock()
        self.canvas.bind("<Left>", lambda _: self.move_left(-1, 0))
        self.canvas.bind("<Right>", lambda _: self.move_right(1, 0))
        self.canvas.bind("<Down>", lambda _: self.move_down(0, 1))
        self.canvas.bind("<Up>", lambda _: self.rotate())
        self.canvas.bind("<space>", lambda _: self.hard_drop(0, 1))

    def draw_game(self):
        self.canvas = tk.Canvas(
            self,
            width=(GAME_WIDTH * BLOCK_SIZE) + 300,
            height=GAME_HEIGHT * BLOCK_SIZE,
            bg="grey",
        )
        self.canvas.focus_set()
        self.canvas.pack(side="left")
        self.canvas.focus_set()
        self.rectangles = [
            self.canvas.create_rectangle(
                (i % GAME_WIDTH) * BLOCK_SIZE,
                (i // GAME_WIDTH) * BLOCK_SIZE,
                ((i % GAME_WIDTH) + 1) * BLOCK_SIZE,
                ((i // GAME_WIDTH) + 1) * BLOCK_SIZE,
            )
            for i in range(GAME_HEIGHT * GAME_WIDTH)
        ]
        self.gui_score = self.canvas.create_text(
            400,
            10,
            text=("Score = " + str(self.game.total_score)),
            fill="white",
            font="Helvetica 10",
        )
        self.gui_lines_eliminated = self.canvas.create_text(
            400,
            30,
            text=("Lines eliminated = " + str(self.game.total_lines_eliminated)),
            fill="white",
            font="Helvetica 10",
        )

    def move_left(self, dx, dy):
        self.game.move_tetromino(dx, dy)
        self.update_game()

    def move_right(self, dx, dy):
        self.game.move_tetromino(dx, dy)
        self.update_game()

    def move_down(self, dx, dy):
        self.game.move_tetromino(dx, dy)
        self.update_game()

    def hard_drop(self, x, y):
        while self.game.move_tetromino(0, 1):
            pass
        self.update_game()

    def clock(self):
        self.move_down(0, 1)
        self.canvas.after(1000, self.clock)

    def rotate(self):
        self.game.rotate()
        self.update_game()

    def update_game(self):
        for i in range(len(self.rectangles)):
            colour_num = self.game.get_colour(i % (GAME_WIDTH), i // GAME_WIDTH)
            self.canvas.itemconfig(self.rectangles[i], fill=COLOURS[colour_num])
        self.canvas.itemconfig(
            self.gui_lines_eliminated,
            text=("Lines eliminated = " + str(self.game.total_lines_eliminated)),
        )
        self.canvas.itemconfig(
            self.gui_score, text=("Score = " + str(self.game.total_score))
        )


root = tk.Tk()
root.title("Tetris")
root.resizable(False, False)
app = Application(master=root)
app.mainloop()
