import tkinter as tk

GRID_SIZE = 5
GROW_TIME_MS = 5000  # 5 seconds for crop to mature

class FarmPatch:
    def __init__(self, master, row, col, harvest_callback):
        self.state = 'empty'  # states: empty, planted, grown
        self.button = tk.Button(master, width=8, height=4, command=self.on_click)
        self.button.grid(row=row, column=col, padx=2, pady=2)
        self.harvest_callback = harvest_callback

    def on_click(self):
        if self.state == 'empty':
            self.plant()
        elif self.state == 'grown':
            self.harvest()

    def plant(self):
        self.state = 'planted'
        self.button.config(text='Seed', bg='saddle brown')
        self.button.after(GROW_TIME_MS, self.grow)

    def grow(self):
        if self.state == 'planted':
            self.state = 'grown'
            self.button.config(text='Crop', bg='forest green')

    def harvest(self):
        if self.state == 'grown':
            self.state = 'empty'
            self.button.config(text='', bg='SystemButtonFace')
            self.harvest_callback()

def main():
    root = tk.Tk()
    root.title('Farming Game')
    score = tk.IntVar(value=0)

    def on_harvest():
        score.set(score.get() + 1)

    patches = []
    for r in range(GRID_SIZE):
        row = []
        for c in range(GRID_SIZE):
            patch = FarmPatch(root, r, c, on_harvest)
            row.append(patch)
        patches.append(row)

    score_label = tk.Label(root, textvariable=score, font=('Arial', 16))
    tk.Label(root, text='Harvested:').grid(row=GRID_SIZE, column=0, columnspan=2, pady=10)
    score_label.grid(row=GRID_SIZE, column=2, columnspan=3, pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()
