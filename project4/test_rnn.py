import unittest
import rnn


class TestRnn(unittest.TestCase):
    def test_rnn(self):
        r = rnn.Rnn(5, 2, 2)
        self.assertEqual(r.num_edges, 26)
        r.set_weights(range(26))
        output_values = r.activate([0, 0, 0, 0, 0])
        self.assertEqual(len(output_values), 2)


if __name__ == '__main__':
    unittest.main()
