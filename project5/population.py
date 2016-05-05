import genotype
import individual

class Population(object):
    def __init__(self):
        self.individuals = None

    def set_individuals(self, individuals):
        self.individuals = individuals

    def get_non_dominated_individuals(self):
        non_dominated_individuals = []
        for i1 in self.individuals:
            # check if i1 is dominated by any other individual
            i1.is_dominated = False
            for i2 in self.individuals:
                if i1 == i2:
                    continue
                if i2.dominates(i1):
                    i1.is_dominated = True
                    break
            if not i1.is_dominated:
                non_dominated_individuals.append(i1)
        return non_dominated_individuals

    def generate_individuals(self, n):
        genotypes = [genotype.Genotype.get_random_genotype() for _ in range(n)]
        individuals = [individual.Individual(g) for g in genotypes]
        self.individuals = individuals

        return individuals

    def calcualte_all_crowding_distances(self, pareto_front):
        pareto_front = sorted(pareto_front, key=lambda x: x.tour_distance)
        pareto_front[0].set_crowding_distance(float("inf"))
        pareto_front[-1].set_crowding_distance(float("inf"))

        max_dist = float(pareto_front[-1].tour_distance)
        min_dist = float(pareto_front[0].tour_distance)

        for i in range(len(self.individuals)):
            self.individuals[i].calculate_crowding_distance(i, pareto_front, max_dist, min_dist)

