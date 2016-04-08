import unittest
import world
import gfx


class TestWorld(unittest.TestCase):
    def test_rendering(self):
        w = world.World()
        x, y, width = 1, 0, 2
        w.set_item(x, y, width)

        agent_x = 2
        w.set_agent(agent_x)

        g = gfx.Gfx(fps=2)
        g.draw(w)
        w.agent.move(-1)
        w.move_item_down()
        g.draw(w)
        w.agent.move(-2)
        w.move_item_down()
        g.draw(w)
        w.agent.move(-3)
        w.move_item_down()
        g.draw(w)
        w.agent.move(-4)
        w.move_item_down()
        g.draw(w)
        g.draw(w)

if __name__ == '__main__':
    unittest.main()
