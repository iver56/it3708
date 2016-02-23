import random
import statistics
import adult_selection
import parent_selection


class Population(object):
    def __init__(self, population_size, problem_class, genotype_class, individual_class, adult_selection_method,
                 parent_selection_method, adult_pool_size, initial_temperature=10.0, cooling_rate=1.0):
        self.genotypes = []
        for x in range(population_size):
            genotype = genotype_class.get_random_genotype(genotype_class.GENOTYPE_SIZE)
            self.genotypes.append(genotype)

        self.problem_class = problem_class
        self.individual_class = individual_class
        self.individuals = None
        self.adult_pool_size = adult_pool_size
        self.population_size = population_size
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.generation = 0
        self.adults = None
        self.parents = None
        self.log = []
        self.adult_selection_handler = adult_selection.AdultSelection(self, adult_selection_method)
        self.parent_selection_handler = parent_selection.ParentSelection(self, parent_selection_method)

    def generate_phenotypes(self):
        self.individuals = []
        for genotype in self.genotypes:
            phenotype = self.individual_class(genotype)
            self.individuals.append(phenotype)

    def evaluate_all(self):
        for phenotype in self.individuals:
            fitness = self.problem_class.calculate_fitness(phenotype)
            phenotype.set_fitness(fitness)

    def get_fittest_individual(self):
        """
        May raise an exception if the population is not evaluated
        :return:
        """
        max_fitness = self.adults[0].fitness
        fittest_individual = self.adults[0]
        for individual in self.adults:
            if individual.fitness > max_fitness:
                max_fitness = individual.fitness
                fittest_individual = individual
        return fittest_individual

    def log_stats(self):
        fittest_individual = self.get_fittest_individual()
        average_fitness = self.get_adults_fitness_avg()
        fitness_std_dev = self.get_adults_fitness_std_dev()
        print 'fittest phenotype:', fittest_individual
        print 'avg fitness =', average_fitness
        print 'fitness standard deviation =', fitness_std_dev
        log_item = {
            'max_fitness': fittest_individual.fitness,
            'avg_fitness': average_fitness,
            'fitness_std_dev': fitness_std_dev
        }
        self.log.append(log_item)

    def get_adults_fitness_sum(self):
        return sum([individual.fitness for individual in self.adults])

    def get_adults_fitness_avg(self):
        return float(self.get_adults_fitness_sum()) / len(self.adults)

    def get_adults_fitness_std_dev(self):
        return statistics.pstdev([individual.fitness for individual in self.adults])

    def set_generation(self, generation):
        self.generation = generation

    def reproduce(self):
        num_children = self.population_size

        self.genotypes = []

        for i in range(num_children):
            random_parent = random.choice(self.adults)
            new_genotype = random_parent.genotype.clone()
            new_genotype.mutate()
            self.genotypes.append(new_genotype)
