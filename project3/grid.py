import random


class Item:
    Nothing = '`'
    Poison = '+'
    Food = '@'

    def __init__(self):
        pass


class Grid(object):
    def __init__(self, n=10, food_probability=0.33, poison_probability=0.33, seed=1):
        self.n = n
        num_cells = n * n
        self.cells = []

        # Initialize cells
        for i in range(num_cells):
            self.cells.append(Item.Nothing)

        random.seed(seed)

        # Add food
        for i in range(num_cells):
            if random.random() < food_probability:
                self.cells[i] = Item.Food
        
        # Add poison to some of the remaining cells
        for i in range(num_cells):
            if self.cells[i] == Item.Nothing and random.random() < poison_probability:
                self.cells[i] = Item.Poison

    def get_cell(self, x, y):
        i = self.n * y + x
        return self.cells[i]

    def __repr__(self):
        s = ''
        for y in range(self.n):
            for x in range(self.n):
                cell = self.get_cell(x, y)
                s += cell + ' '
            s += '\n'
        return s
