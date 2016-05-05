from data_manager import dm


class Individual(object):
    def __init__(self, genotype):
        self.genotype = genotype

    def calculate_tour_distance(self):
        # TODO: should be sped up by caching
        return sum(
            dm.get_distance(self.genotype.city_ids[i], self.genotype.city_ids[i + 1])
            for i in range(len(self.genotype.city_ids) - 1)
        )

    def calculate_tour_cost(self):
        # TODO: should be sped up by caching
        return sum(
            dm.get_cost(self.genotype.city_ids[i], self.genotype.city_ids[i + 1])
            for i in range(len(self.genotype.city_ids) - 1)
        )

    def dominates(self, other_individual):
        return (
            self.calculate_tour_distance() <= other_individual.calculate_tour_distance() and  # distance not worse
            self.calculate_tour_cost() <= other_individual.calculate_tour_cost() and  # cost not worse
            (
                self.calculate_tour_distance() < other_individual.calculate_tour_distance() or  # distance is better
                self.calculate_tour_cost() < other_individual.calculate_tour_cost()  # cost is better
            )
        )
