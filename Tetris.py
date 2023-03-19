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
        [(1, 0), (1, 1), (1, 2), (2, 2)],  # L
        [(1, 1), (0, 2), (0, 1), (2, 1)],  # L first turn
        [(1, 1), (0, 0), (1, 0), (1, 2)],  # L second turn
        [(1, 1), (0, 1), (2, 1), (2, 0)],  # L third turn
    ],
    [
        [(0, 2), (1, 2), (1, 1), (1, 0)],  # J
        [(0, 0), (0, 1), (1, 1), (2, 1)],  # J first turn
        [(1, 0), (2, 0), (1, 1), (1, 2)],  # J second turn
        [(0, 1), (1, 1), (2, 1), (2, 2)],  # J third turn
    ],
    [
        [(0, 1), (1, 1), (2, 1), (1, 2)],  # T
        [(1, 0), (1, 1), (1, 2), (0, 1)],  # T first turn
        [(0, 1), (1, 1), (1, 0), (2, 1)],  # T second turn
        [(1, 0), (1, 1), (1, 2), (2, 1)],  # T third turn
    ],
    [
        [(1, 1), (1, 0), (1, 2), (1, 3)],  # I
        [(1, 1), (0, 1), (2, 1), (3, 1)],  # I first turn
        [(1, 1), (1, 0), (1, 2), (1, 3)],  # I second turn
        [(1, 1), (0, 1), (2, 1), (3, 1)],  # I third turn
    ],
    [
        [(1, 1), (1, 0), (0, 1), (2, 0)],  # S
        [(0, 0), (0, 1), (1, 1), (1, 2)],  # S first turn
        [(1, 1), (1, 0), (0, 1), (2, 0)],  # S second turn
        [(0, 0), (0, 1), (1, 1), (1, 2)],  # S third turn
    ],
    [
        [(0, 0), (1, 0), (1, 1), (2, 1)],  # Z
        [(1, 1), (0, 1), (1, 0), (0, 2)],  # Z first turn
        [(0, 0), (1, 0), (1, 1), (2, 1)],  # Z second turn
        [(1, 1), (0, 1), (1, 0), (0, 2)],  # Z third turn
    ],
]

UNGRABBED_BAG = [0, 1, 2, 3, 4, 5, 6]
TETROMINOID_LIST = [0]
COLOURID_LIST = [0]


class Game:
    def __init__(self):
        self.grid = [[0 for x in range(GAME_WIDTH)] for y in range(GAME_HEIGHT)]
        self.next_tetromino_grid = [[0 for c in range(4)] for r in range(4)]
        self.choose_piece()
        self.choose_colour()
        self.make_tetromino()
        self.total_score = 0
        self.total_lines_eliminated = 0
        self.game_level = 0
        self.score_multiplier = [0, 40, 100, 300, 1200]
        self.next_tetromino_offset = [0, 0]

    def choose_piece(self):
        global UNGRABBED_BAG
        if len(UNGRABBED_BAG) == 0:
            UNGRABBED_BAG = [0, 1, 2, 3, 4, 5, 6]
        pop_value1 = random.randint(0, len(UNGRABBED_BAG) - 1)
        TETROMINOID_LIST.append(UNGRABBED_BAG.pop(pop_value1))
        self.tetromino_id = TETROMINOID_LIST[0]

    def choose_colour(self):
        self.piece_colour_rand = random.randint(1, len(COLOURS) - 1)
        COLOURID_LIST.append(self.piece_colour_rand)
        self.piece_colour = COLOURID_LIST[0]
        self.next_tetromino_colour = COLOURID_LIST[1]

    def make_tetromino(self):
        COLOURID_LIST.remove(COLOURID_LIST[0])
        self.choose_colour()
        self.current_coord = [GAME_WIDTH // 2, 0]
        TETROMINOID_LIST.remove(TETROMINOID_LIST[0])
        self.choose_piece()
        self.rotation_id = 0
        self.tetromino = TETROMINOS[self.tetromino_id][self.rotation_id]
        self.next_tetromino = TETROMINOS[TETROMINOID_LIST[1]][0]

    def get_next_tetromino_coords(self):
        return [
            (r + self.next_tetromino_offset[0], c + self.next_tetromino_offset[1])
            for r, c in self.next_tetromino
        ]

    def get_tetromino_coords(self):
        return [
            (x + self.current_coord[0], y + self.current_coord[1])
            for x, y in self.tetromino
        ]

    def get_next_tetromino_colour(self, r, c):
        return (
            self.next_tetromino_colour
            if (c, r) in self.get_next_tetromino_coords()
            else self.next_tetromino_grid[c][r]
        )

    def set_colour(self):
        for x, y in self.get_tetromino_coords():
            self.grid[y][x] = self.piece_colour
        new_grid = [row for row in self.grid if any(tile == 0 for tile in row)]
        lines_eliminated = len(self.grid) - len(new_grid)
        score = self.score_multiplier[lines_eliminated]
        self.total_score += score
        self.total_lines_eliminated += lines_eliminated
        self.game_level = self.total_lines_eliminated // 10
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

    def rotate_clockwise(self):
        self.rotation_id = (self.rotation_id + 1) % 4
        self.tetromino = TETROMINOS[self.tetromino_id][self.rotation_id]

    def rotate_anticlockwise(self):
        self.rotation_id = (self.rotation_id - 1) % 4
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
        self.canvas.bind("<Up>", lambda _: self.rotate_clockwise())
        self.canvas.bind("<x>", lambda _: self.rotate_clockwise())
        self.canvas.bind("<z>", lambda _: self.rotate_anticlockwise())
        self.canvas.bind("<space>", lambda _: self.hard_drop(0, 1))

    def draw_game(self):
        self.canvas = tk.Canvas(
            self,
            width=(GAME_WIDTH * BLOCK_SIZE) + 300,
            height=GAME_HEIGHT * BLOCK_SIZE,
            bg=COLOURS[0],
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
                outline="",
            )
            for i in range(GAME_HEIGHT * GAME_WIDTH)
        ]
        # self.next_piece_rectangle_border = self.canvas.create_rectangle(390, 179, 511, 300, outline='white')
        self.next_piece_grid = [
            self.canvas.create_rectangle(
                391 + (i % 4) * BLOCK_SIZE,
                180 + (i // 4) * BLOCK_SIZE,
                391 + ((i % 4) + 1) * BLOCK_SIZE,
                180 + ((i // 4) + 1) * BLOCK_SIZE,
                fill="",
                outline="",
            )
            for i in range(16)
        ]
        line1 = self.canvas.create_line(300, 0, 300, 665, fill="white", width=1)
        line2 = self.canvas.create_line(300, 120, 600, 120, fill="white", width=1)
        line3 = self.canvas.create_line(300, 330, 600, 330, fill="white", width=1)
        self.gui_score = self.canvas.create_text(
            450,
            30,
            text=("SCORE = " + str(self.game.total_score)),
            fill="white",
            font="Helvetica 20 bold",
        )
        self.gui_lines_eliminated = self.canvas.create_text(
            450,
            60,
            text=("LINES ELIMINATED = " + str(self.game.total_lines_eliminated)),
            fill="white",
            font="Helvetica 20 bold",
        )
        self.gui_game_level = self.canvas.create_text(
            450,
            90,
            text=("LEVEL = " + str(self.game.game_level)),
            fill="white",
            font="Helvetica 20 bold",
        )
        self.gui_next_piece = self.canvas.create_text(
            450,
            150,
            text=("NEXT PIECE"),
            fill="white",
            font="Helvetica 20 bold",
        )
        """
        self.gui_how_to_play = self.canvas.create_text(
            450,
            360,
            text=("KEYBINDS"),
            fill="white",
            font="Helvetica 20 bold",
        )
        self.gui_how_to_play1 = self.canvas.create_text(
            450,
            460,
            text=("• Left = move left\n• Right = move right\n• Down = move down\n• Up = rotate 90° clockwise\n• X = rotate 90° clockwise\n• Z = rotate 90° counterclockwise\n• Space = hard drop"),
            fill="white",
            font="Helvetica 18",
        )
        """

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
        self.canvas.after(int(1000 * (0.66 ** (self.game.game_level))), self.clock)

    def rotate_clockwise(self):
        self.game.rotate_clockwise()
        self.update_game()

    def rotate_anticlockwise(self):
        self.game.rotate_anticlockwise()
        self.update_game()

    def update_game(self):
        for i in range(len(self.rectangles)):
            colour_num1 = self.game.get_colour(i % (GAME_WIDTH), i // GAME_WIDTH)
            self.canvas.itemconfig(self.rectangles[i], fill=COLOURS[colour_num1])

        for i, _id in enumerate(self.next_piece_grid):
            colour_num2 = self.game.get_next_tetromino_colour((i // 4), (i % 4))
            self.canvas.itemconfig(_id, fill=COLOURS[colour_num2])

        self.canvas.itemconfig(
            self.gui_lines_eliminated,
            text=("LINES ELIMINATED = " + str(self.game.total_lines_eliminated)),
        )
        self.canvas.itemconfig(
            self.gui_score, text=("SCORE = " + str(self.game.total_score))
        )
        self.canvas.itemconfig(
            self.gui_game_level, text=("LEVEL = " + str(self.game.game_level))
        )


root = tk.Tk()
root.title("Tetris")
root.resizable(False, False)
app = Application(master=root)
app.mainloop()
