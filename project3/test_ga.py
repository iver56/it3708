import unittest
import ga


class TestFlatlandProblem(unittest.TestCase):
    def test_fitness(self):
        pass  # TODO

    def test_phenotype(self):
        g1 = ga.FlatLandGenotype(ga.FlatLandGenotype.GENOTYPE_SIZE)
        individual = ga.FlatLandIndividual(g1)
        self.assertAlmostEqual(individual.phenotype.weights[0], -2)


if __name__ == '__main__':
    unittest.main()
