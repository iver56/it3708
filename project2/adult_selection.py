class AdultSelection(object):
    def __init__(self, population, adult_selection_method):
        self.population = population
        if adult_selection_method == 'generational_mixing':
            self.adult_selection_method = self.generational_mixing
        elif adult_selection_method == 'over_production':
            self.adult_selection_method = self.over_production
        elif adult_selection_method == 'full_generational_replacement':
            self.adult_selection_method = self.full_generational_replacement

    def select_adults(self):
        self.adult_selection_method()
        for individual in self.population.adults:
            individual.genotype.increase_age()
        return self.population.adults

    def generational_mixing(self):
        all_individuals = (self.population.adults if self.population.adults else []) + self.population.individuals
        sorted_individuals = sorted(all_individuals, key=lambda p: p.fitness, reverse=True)
        self.population.adults = sorted_individuals[0:self.population.adult_pool_size]
        return self.population.adults

    def over_production(self):
        children = filter(lambda individual: individual.genotype.age == 0, self.population.individuals)
        sorted_phenotypes = sorted(children, key=lambda p: p.fitness, reverse=True)
        self.population.adults = sorted_phenotypes[0:self.population.adult_pool_size]
        return self.population.adults

    def full_generational_replacement(self):
        self.population.adults = self.population.individuals
        return self.population.adults
