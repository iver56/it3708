from data_manager import dm


class Individual(object):
    def __init__(self, genotype):
        self.genotype = genotype

    def calculate_tour_distance(self):
        return sum(
            dm.get_distance(i, i + 1)
            for i in range(len(self.genotype.city_ids) - 1)
        )

    def calculate_tour_cost(self):
        return sum(
            dm.get_cost(i, i + 1)
            for i in range(len(self.genotype.city_ids) - 1)
        )
