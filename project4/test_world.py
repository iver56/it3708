import unittest
import world


class TestWorld(unittest.TestCase):
    def test_agent(self):
        w = world.World()
        x, y, width = 1, 0, 2
        w.set_item(x, y, width)

        self.assertEqual(w.is_shadowed(0), False)
        self.assertEqual(w.is_shadowed(1), True)
        self.assertEqual(w.is_shadowed(2), True)
        self.assertEqual(w.is_shadowed(3), False)

        agent_x = 2
        w.set_agent(agent_x)
        positions = w.agent.get_occupied_x_positions()
        self.assertTrue(0 not in positions)
        self.assertTrue(1 not in positions)
        self.assertTrue(2 in positions)
        self.assertTrue(3 in positions)
        self.assertTrue(4 in positions)
        self.assertTrue(5 in positions)
        self.assertTrue(6 in positions)
        self.assertTrue(7 not in positions)

        self.assertEqual(w.agent.sense(), (1, 0, 0, 0, 0))

        # test agent wraparound
        w.agent.move(-3)
        self.assertEqual(w.agent.x, world.World.WIDTH - 1)

        positions = w.agent.get_occupied_x_positions()
        self.assertTrue(0 in positions)
        self.assertTrue(1 in positions)
        self.assertTrue(2 in positions)
        self.assertTrue(3 in positions)
        self.assertTrue(4 not in positions)
        self.assertTrue(5 not in positions)
        self.assertTrue(6 not in positions)
        self.assertTrue(7 not in positions)

        self.assertTrue((world.World.WIDTH - 1) in positions)
        self.assertTrue((world.World.WIDTH - 2) not in positions)

if __name__ == '__main__':
    unittest.main()
