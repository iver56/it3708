import unittest
from grid import Grid
from gfx import Gfx
from agent import Agent
import random


class TestGfx(unittest.TestCase):
    def test_gfx(self):
        my_grid = Grid()
        my_gfx = Gfx(fps=4)
        my_agent = Agent()
        my_agent.set_grid(my_grid)
        for i in range(15):
            r = random.randint(0, 2)
            relative_direction = (r - 1) * 90
            my_agent.move(relative_direction)

            my_gfx.draw(my_grid, my_agent)


if __name__ == '__main__':
    unittest.main()
