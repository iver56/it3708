import genotype
import individual
import random


class Population(object):
    def __init__(self, population_size, crossover_rate, mutation_rate, individuals=None):
        if individuals is None:
            # generate random individuals
            genotypes = [genotype.Genotype.get_random_genotype() for _ in range(population_size)]
            individuals = [individual.Individual(g) for g in genotypes]
            self.individuals = individuals
        else:
            self.individuals = individuals

        self.population_size = len(self.individuals)

        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_selection_k = 2
        self.tournament_selection_epsilon = 0.1
        self.parents = []

    def set_individuals(self, individuals):
        # TODO: this method is deprecated. Remove it.
        self.individuals = individuals

    def get_non_dominated_individuals(self):
        # TODO: This method is deprecated. Remove it. Use fast_non_dominated_sort instead.
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
        # TODO: remove this function
        raise Exception('Removed. Use constructor with individuals=None instead')

    def calculate_all_crowding_distances(self, pareto_front):
        for i in range(2):
            pareto_front = sorted(pareto_front, key=lambda x: x.objectives[i])
            pareto_front[0].set_crowding_distance(float("inf"))
            pareto_front[-1].set_crowding_distance(float("inf"))

            max_dist = float(pareto_front[-1].objectives[i])
            min_dist = float(pareto_front[0].objectives[i])

            for j in range(1, len(pareto_front) - 2):
                pareto_front[j].calculate_crowding_distance(j, pareto_front, max_dist, min_dist, i)

    def fast_non_dominated_sort(self):
        """
        After having run this, each individual is assigned a rank (1 is best while 2, 3 etc are worse)
        The function returns a "fronts" dictionary which contains a set of individuals for each rank
        """
        fronts = {
            1: set()
        }
        for p in self.individuals:
            p.individuals_dominated = set()
            p.domination_counter = 0
            for q in self.individuals:
                if p.dominates(q):
                    p.individuals_dominated.add(q)
                elif q.dominates(p):
                    p.domination_counter += 1
            if p.domination_counter == 0:
                p.rank = 1
                fronts[1].add(p)
        i = 1
        while len(fronts[i]) != 0:
            new_front = set()
            for p in fronts[i]:
                for q in p.individuals_dominated:
                    q.domination_counter -= 1
                    if q.domination_counter == 0:
                        q.rank = i + 1
                        new_front.add(q)
            i += 1
            fronts[i] = new_front
        return fronts

    def create_offspring(self):
        self.tournament_selection()  # select parents

        genotypes = []
        for i in range(len(self.individuals)):
            new_genotype = self.produce_one_child_genotype()
            genotypes.append(new_genotype)
        return genotypes

    def produce_one_child_genotype(self):
        if random.random() < self.crossover_rate:
            parents = random.sample(self.parents, 2)
            new_genotype = parents[0].genotype.clone()
            new_genotype.crossover(parents[1].genotype)
        else:
            random_parent = random.choice(self.parents)
            new_genotype = random_parent.genotype.clone()

        if random.random() < self.mutation_rate:
            new_genotype.mutate()

        return new_genotype

    def tournament_selection(self):
        self.parents = []
        for i in range(len(self.individuals)):
            parent = self.do_one_tournament()
            self.parents.append(parent)

    def do_one_tournament(self):
        contestants = random.sample(self.individuals, self.tournament_selection_k)
        r = random.random()
        if r < self.tournament_selection_epsilon:
            return random.choice(contestants)
        else:
            sorted_contestants = sorted(contestants, key=lambda p: p.rank)  # TODO: sort by rank, then crowding distance
            return sorted_contestants[0]
