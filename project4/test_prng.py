import unittest
import prng


class TestPrng(unittest.TestCase):
    def test_prng(self):
        p1 = prng.Prng(seed=1)
        random_ints_1 = [p1.randint(0, 9) for _ in range(20)]
        p2 = prng.Prng(seed=2)
        random_ints_2 = [p2.randint(0, 9) for _ in range(20)]
        self.assertNotEqual(random_ints_1, random_ints_2)

        p1b = prng.Prng(seed=1)
        random_ints_1b = [p1b.randint(0, 9) for _ in range(20)]
        self.assertEqual(random_ints_1, random_ints_1b)

        p1c = prng.Prng(seed=1)
        random_ints_1c = [p1c.randint(0, 9) for _ in range(10)]
        p2c = prng.Prng(seed=2)
        [p2c.randint(0, 9) for _ in range(10)]
        random_ints_1c += [p1c.randint(0, 9) for _ in range(10)]
        self.assertEqual(random_ints_1, random_ints_1c)


if __name__ == '__main__':
    unittest.main()
