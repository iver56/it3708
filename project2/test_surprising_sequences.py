import unittest
import surprising_sequences


class TestSurprisingSequencesProblem(unittest.TestCase):
    def test_fitness1(self):
        alphabet_size = 3
        surprising_sequences.SurprisingSequencesGenotype.set_alphabet(alphabet_size)
        g = surprising_sequences.SurprisingSequencesGenotype(3)
        g.dna = ['A', 'B', 'C']
        p = surprising_sequences.SurprisingSequencesIndividual(g)
        fitness1 = surprising_sequences.SurprisingSequencesProblem.calculate_fitness(p)
        self.assertAlmostEqual(fitness1, 1.0)  # surprising

    def test_fitness2(self):
        alphabet_size = 3
        surprising_sequences.SurprisingSequencesGenotype.set_alphabet(alphabet_size)
        g1 = surprising_sequences.SurprisingSequencesGenotype(3)
        g1.dna = ['A', 'B', 'C', 'C', 'B', 'A']
        p1 = surprising_sequences.SurprisingSequencesIndividual(g1)
        fitness1 = surprising_sequences.SurprisingSequencesProblem.calculate_fitness(p1)
        self.assertAlmostEqual(fitness1, 1.0)  # surprising

    def test_fitness3(self):
        alphabet_size = 3
        surprising_sequences.SurprisingSequencesGenotype.set_alphabet(alphabet_size)
        g1 = surprising_sequences.SurprisingSequencesGenotype(3)
        g1.dna = ['A', 'A', 'B', 'C', 'C']
        p1 = surprising_sequences.SurprisingSequencesIndividual(g1)
        fitness1 = surprising_sequences.SurprisingSequencesProblem.calculate_fitness(p1)
        self.assertLess(fitness1, 1.0)  # not surprising

    def test_fitness4(self):
        alphabet_size = 3
        surprising_sequences.SurprisingSequencesGenotype.set_alphabet(alphabet_size)
        g1 = surprising_sequences.SurprisingSequencesGenotype(3)
        g1.dna = ['A', 'B', 'B', 'A', 'C', 'C', 'A']
        p1 = surprising_sequences.SurprisingSequencesIndividual(g1)
        fitness1 = surprising_sequences.SurprisingSequencesProblem.calculate_fitness(p1)
        self.assertLess(fitness1, 1.0)  # not surprising

    def test_phenotype(self):
        g1 = surprising_sequences.SurprisingSequencesGenotype(3)
        g1.dna = ['A', 'B', 'C']
        individual = surprising_sequences.SurprisingSequencesIndividual(g1)
        self.assertEqual(individual.phenotype, ['A', 'B', 'C'])


if __name__ == '__main__':
    unittest.main()
