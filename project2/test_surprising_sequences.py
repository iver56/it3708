import unittest
import surprising_sequences


class TestSurprisingSequencesProblem(unittest.TestCase):
    def test_fitness_global1(self):
        surprising_sequences.SurprisingSequencesProblem.MODE = 'global'
        alphabet_size = 3
        surprising_sequences.SurprisingSequencesGenotype.set_alphabet(alphabet_size)
        g = surprising_sequences.SurprisingSequencesGenotype(3)
        g.dna = ['A', 'B', 'C']
        p = surprising_sequences.SurprisingSequencesIndividual(g)
        fitness = surprising_sequences.SurprisingSequencesProblem.calculate_fitness(p)
        self.assertAlmostEqual(fitness, 1.0)  # surprising

    def test_fitness_global2(self):
        surprising_sequences.SurprisingSequencesProblem.MODE = 'global'
        alphabet_size = 3
        surprising_sequences.SurprisingSequencesGenotype.set_alphabet(alphabet_size)
        g = surprising_sequences.SurprisingSequencesGenotype(3)
        g.dna = ['A', 'B', 'C', 'C', 'B', 'A']
        p = surprising_sequences.SurprisingSequencesIndividual(g)
        fitness = surprising_sequences.SurprisingSequencesProblem.calculate_fitness(p)
        self.assertAlmostEqual(fitness, 1.0)  # surprising

    def test_fitness_global3(self):
        surprising_sequences.SurprisingSequencesProblem.MODE = 'global'
        alphabet_size = 3
        surprising_sequences.SurprisingSequencesGenotype.set_alphabet(alphabet_size)
        g = surprising_sequences.SurprisingSequencesGenotype(3)
        g.dna = ['A', 'A', 'B', 'C', 'C']
        p = surprising_sequences.SurprisingSequencesIndividual(g)
        fitness = surprising_sequences.SurprisingSequencesProblem.calculate_fitness(p)
        self.assertLess(fitness, 1.0)  # not surprising

    def test_fitness_global4(self):
        surprising_sequences.SurprisingSequencesProblem.MODE = 'global'
        alphabet_size = 3
        surprising_sequences.SurprisingSequencesGenotype.set_alphabet(alphabet_size)
        g = surprising_sequences.SurprisingSequencesGenotype(3)
        g.dna = ['A', 'B', 'B', 'A', 'C', 'C', 'A']
        p = surprising_sequences.SurprisingSequencesIndividual(g)
        fitness = surprising_sequences.SurprisingSequencesProblem.calculate_fitness(p)
        self.assertLess(fitness, 1.0)  # not surprising

    def test_fitness_local1(self):
        surprising_sequences.SurprisingSequencesProblem.MODE = 'local'
        alphabet_size = 3
        surprising_sequences.SurprisingSequencesGenotype.set_alphabet(alphabet_size)
        g = surprising_sequences.SurprisingSequencesGenotype(3)
        g.dna = ['A', 'A', 'B', 'C', 'C']
        p = surprising_sequences.SurprisingSequencesIndividual(g)
        fitness = surprising_sequences.SurprisingSequencesProblem.calculate_fitness(p)
        self.assertAlmostEqual(fitness, 1.0)  # surprising

    def test_fitness_local2(self):
        surprising_sequences.SurprisingSequencesProblem.MODE = 'local'
        alphabet_size = 3
        surprising_sequences.SurprisingSequencesGenotype.set_alphabet(alphabet_size)
        g = surprising_sequences.SurprisingSequencesGenotype(3)
        g.dna = ['A', 'B', 'B', 'A', 'C', 'C', 'A']
        p = surprising_sequences.SurprisingSequencesIndividual(g)
        fitness = surprising_sequences.SurprisingSequencesProblem.calculate_fitness(p)
        self.assertAlmostEqual(fitness, 1.0)  # surprising

    def test_fitness_local3(self):
        surprising_sequences.SurprisingSequencesProblem.MODE = 'local'
        alphabet_size = 3
        surprising_sequences.SurprisingSequencesGenotype.set_alphabet(alphabet_size)
        g = surprising_sequences.SurprisingSequencesGenotype(3)
        g.dna = ['A', 'B', 'C', 'B', 'C']
        p = surprising_sequences.SurprisingSequencesIndividual(g)
        fitness = surprising_sequences.SurprisingSequencesProblem.calculate_fitness(p)
        self.assertLess(fitness, 1.0)  # not surprising

    def test_phenotype(self):
        g1 = surprising_sequences.SurprisingSequencesGenotype(3)
        g1.dna = ['A', 'B', 'C']
        individual = surprising_sequences.SurprisingSequencesIndividual(g1)
        self.assertEqual(individual.phenotype, ['A', 'B', 'C'])


if __name__ == '__main__':
    unittest.main()
