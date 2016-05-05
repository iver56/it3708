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
