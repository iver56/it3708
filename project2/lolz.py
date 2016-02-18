from individual import Individual
from problem import Problem


class LolzProblem(Problem):
    GENOTYPE_SIZE = 6
    ZERO_CAP = 4

    @staticmethod
    def calculate_fitness(individual):
        zero_score = 0
        one_score = 0
        zero_streak = True
        one_streak = True

        for x in individual.phenotype:
            if x == 0 and zero_streak:
                zero_score += 1
                one_streak = False
            elif x == 1 and one_streak:
                one_score += 1
                zero_streak = False
            else:
                break

        if zero_score > LolzProblem.ZERO_CAP:
            zero_score = LolzProblem.ZERO_CAP

        return max(zero_score, one_score)


class LolzIndividual(Individual):
    def calculate_phenotype(self):
        self.phenotype = map(lambda x: 1 if x else 0, self.genotype.dna)
