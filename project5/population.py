class Population(object):
    def __init__(self):
        self.individuals = None

    def set_individuals(self, individuals):
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
