import unittest
import agent
import grid


class TestAgent(unittest.TestCase):
    def test_agent(self):
        a = agent.Agent()
        g = grid.Grid()
        a.set_grid(g)

        init_x = a.x
        init_y = a.y
        a.move(0)
        self.assertEqual(a.x, init_x + 1)
        self.assertEqual(a.y, init_y)
        a.move(-90)
        self.assertEqual(a.x, init_x + 1)
        self.assertEqual(a.y, init_y + 1)

        # test wrap around
        for i in range(20):
            a.move(0)
            self.assertLess(a.x, grid.Grid.WIDTH)
            self.assertLess(a.y, grid.Grid.HEIGHT)

if __name__ == '__main__':
    unittest.main()
