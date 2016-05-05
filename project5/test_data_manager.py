import unittest
import data_manager


class TestDataManager(unittest.TestCase):
    def test_lower_triangular_matrix_lookup(self):
        dm = data_manager.DataManager()

        self.assertEqual(dm.get_cost(1, 1), 0)
        self.assertEqual(dm.get_cost(6, 4), 67)
        self.assertEqual(dm.get_cost(4, 6), 67)
        with self.assertRaises(ValueError):
            self.assertEqual(dm.get_cost(0, 0), 0)

        self.assertEqual(dm.get_distance(1, 1), 0)
        self.assertEqual(dm.get_distance(10, 13), 3648)
        self.assertEqual(dm.get_distance(13, 10), 3648)
        with self.assertRaises(ValueError):
            self.assertEqual(dm.get_distance(0, 0), 0)


if __name__ == '__main__':
    unittest.main()
