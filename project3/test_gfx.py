import unittest
from grid import Grid
from gfx import Gfx


class TestGfx(unittest.TestCase):
    def test_gfx(self):
        my_grid = Grid()
        my_gfx = Gfx()
        for i in range(15):
            my_gfx.draw(my_grid)


if __name__ == '__main__':
    unittest.main()
