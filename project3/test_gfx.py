import unittest
from grid import Grid
from gfx import Gfx
from agent import Agent


class TestGfx(unittest.TestCase):
    def test_gfx(self):
        my_grid = Grid()
        my_gfx = Gfx()
        my_agent = Agent()
        for i in range(15):
            my_gfx.draw(my_grid, my_agent)


if __name__ == '__main__':
    unittest.main()
