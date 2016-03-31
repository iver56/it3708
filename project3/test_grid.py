import unittest
from grid import Grid


class TestGrid(unittest.TestCase):
    def test_grid(self):
        g = Grid()
        print g

if __name__ == '__main__':
    unittest.main()
