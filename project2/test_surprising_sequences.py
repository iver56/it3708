import unittest
import surprising_sequences


class TestSurprisingSequencesProblem(unittest.TestCase):
    def assert_fitness(self, mode, dna, should_be_surprising):
        surprising_sequences.SurprisingSequencesProblem.MODE = mode
        alphabet_size = 3
        surprising_sequences.SurprisingSequencesGenotype.set_alphabet(alphabet_size)
        g = surprising_sequences.SurprisingSequencesGenotype(3)
        g.dna = dna
        p = surprising_sequences.SurprisingSequencesIndividual(g)
        fitness = surprising_sequences.SurprisingSequencesProblem.calculate_fitness(p)
        if should_be_surprising:
            self.assertAlmostEqual(fitness, 1.0)
        else:
            self.assertLess(fitness, 1.0)

    def test_fitness_global1(self):
        self.assert_fitness('global', ['A', 'B', 'C'], should_be_surprising=True)

    def test_fitness_global2(self):
        self.assert_fitness('global', ['A', 'B', 'C', 'C', 'B', 'A'], should_be_surprising=True)

    def test_fitness_global3(self):
        self.assert_fitness('global', ['A', 'A', 'B', 'C', 'C'], should_be_surprising=False)

    def test_fitness_global4(self):
        self.assert_fitness('global', ['A', 'B', 'B', 'A', 'C', 'C', 'A'], should_be_surprising=False)

    def test_fitness_local1(self):
        self.assert_fitness('local', ['A', 'A', 'B', 'C', 'C'], should_be_surprising=True)

    def test_fitness_local2(self):
        self.assert_fitness('local', ['A', 'B', 'B', 'A', 'C', 'C', 'A'], should_be_surprising=True)

    def test_fitness_local3(self):
        self.assert_fitness('local', ['A', 'B', 'C', 'B', 'C'], should_be_surprising=False)

    def test_phenotype(self):
        g1 = surprising_sequences.SurprisingSequencesGenotype(3)
        g1.dna = ['A', 'B', 'C']
        individual = surprising_sequences.SurprisingSequencesIndividual(g1)
        self.assertEqual(individual.phenotype, ['A', 'B', 'C'])


if __name__ == '__main__':
    unittest.main()
