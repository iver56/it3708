import unittest
import rnn


class TestRnn(unittest.TestCase):
    def test_rnn(self):
        r = rnn.Rnn(5, 2, 2)
        self.assertEqual(r.num_edges, 34)
        r.set_weights(range(34))
        output_values = r.activate([0, 0, 0, 0, 0])
        self.assertEqual(len(output_values), 2)
        for output_value in output_values:
            self.assertLessEqual(output_value, 1.0)


if __name__ == '__main__':
    unittest.main()
