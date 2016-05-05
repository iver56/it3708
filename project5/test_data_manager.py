import unittest
import data_manager


class TestDataManager(unittest.TestCase):
    def test_lower_triangular_matrix_lookup(self):
        dm = data_manager.dm

        self.assertEqual(dm.get_cost(0, 0), 0)
        self.assertEqual(dm.get_cost(1, 1), 0)
        self.assertEqual(dm.get_cost(5, 3), 67)
        self.assertEqual(dm.get_cost(3, 5), 67)

        self.assertEqual(dm.get_distance(0, 0), 0)
        self.assertEqual(dm.get_distance(1, 1), 0)
        self.assertEqual(dm.get_distance(9, 12), 3648)
        self.assertEqual(dm.get_distance(12, 9), 3648)

    def test_num_cities(self):
        self.assertEqual(data_manager.dm.num_cities, 48)
        self.assertEqual(len(data_manager.dm.city_ids), 48)


if __name__ == '__main__':
    unittest.main()
