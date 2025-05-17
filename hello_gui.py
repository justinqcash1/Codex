import tkinter as tk
import random

# Constants
CELL_SIZE = 30
COLUMNS = 10
ROWS = 20
DELAY = 500  # milliseconds between automatic moves

# Tetromino definitions (shape matrices with numeric codes for colors)
TETROMINOES = [
    [[1, 1, 1, 1]],  # I
    [[0, 2], [0, 2], [2, 2]],  # J
    [[3, 0], [3, 0], [3, 3]],  # L
    [[4, 4], [4, 4]],          # O
    [[0, 5, 5], [5, 5, 0]],    # S
    [[0, 6, 0], [6, 6, 6]],    # T
    [[7, 7, 0], [0, 7, 7]],    # Z
]

COLORS = {
    1: "cyan",
    2: "blue",
    3: "orange",
    4: "yellow",
    5: "green",
    6: "purple",
    7: "red",
}

class Tetris:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.canvas = tk.Canvas(root, width=CELL_SIZE * COLUMNS, height=CELL_SIZE * ROWS)
        self.canvas.pack()

        self.board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current = None
        self.cur_row = 0
        self.cur_col = 0
        self.game_over = False

        self.root.bind("<Left>", lambda _: self.move(0, -1))
        self.root.bind("<Right>", lambda _: self.move(0, 1))
        self.root.bind("<Down>", lambda _: self.move(1, 0))
        self.root.bind("<Up>", lambda _: self.rotate())

        self.spawn_piece()
        self.update()

    def spawn_piece(self):
        self.current = [row[:] for row in random.choice(TETROMINOES)]
        self.cur_row = 0
        self.cur_col = (COLUMNS - len(self.current[0])) // 2
        if self.collision(self.cur_row, self.cur_col, self.current):
            self.game_over = True

    def rotate(self):
        if self.current is None:
            return
        rotated = [list(row) for row in zip(*self.current[::-1])]
        if not self.collision(self.cur_row, self.cur_col, rotated):
            self.current = rotated
            self.draw()

    def move(self, dr: int, dc: int):
        if self.current is None:
            return
        new_row = self.cur_row + dr
        new_col = self.cur_col + dc
        if not self.collision(new_row, new_col, self.current):
            self.cur_row = new_row
            self.cur_col = new_col
            self.draw()
        elif dr == 1 and dc == 0:  # moving down and collided
            self.lock_piece()

    def lock_piece(self):
        for r, row in enumerate(self.current):
            for c, val in enumerate(row):
                if val:
                    self.board[self.cur_row + r][self.cur_col + c] = val
        self.clear_lines()
        self.spawn_piece()
        self.draw()

    def clear_lines(self):
        new_board = [row for row in self.board if any(v == 0 for v in row)]
        lines_cleared = ROWS - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [0 for _ in range(COLUMNS)])
        self.board = new_board

    def collision(self, test_row: int, test_col: int, shape):
        for r, row in enumerate(shape):
            for c, val in enumerate(row):
                if val:
                    br = test_row + r
                    bc = test_col + c
                    if br < 0 or br >= ROWS or bc < 0 or bc >= COLUMNS:
                        return True
                    if self.board[br][bc]:
                        return True
        return False

    def draw(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLUMNS):
                val = self.board[r][c]
                if val:
                    self.draw_cell(r, c, COLORS[val])
        if self.current:
            for r, row in enumerate(self.current):
                for c, val in enumerate(row):
                    if val:
                        self.draw_cell(self.cur_row + r, self.cur_col + c, COLORS[val])
        if self.game_over:
            self.canvas.create_text(
                CELL_SIZE * COLUMNS / 2,
                CELL_SIZE * ROWS / 2,
                text="Game Over",
                fill="red",
                font=("Arial", 24),
            )

    def draw_cell(self, row: int, col: int, color: str):
        x1 = col * CELL_SIZE
        y1 = row * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def update(self):
        if not self.game_over:
            self.move(1, 0)
            self.root.after(DELAY, self.update)
        self.draw()


def main():
    root = tk.Tk()
    root.title("Tetris")
    Tetris(root)
    root.mainloop()


if __name__ == "__main__":
    main()
