import unittest
import ann


class TestAnn(unittest.TestCase):
    def test_ann(self):
        a = ann.Ann(3, 3)
        output_values = a.activate([0, 0, 0])
        print output_values
        for output_value in output_values:
            self.assertGreater(output_value, 0)
        self.assertAlmostEqual(output_values[0], output_values[1])

if __name__ == '__main__':
    unittest.main()
