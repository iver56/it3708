from data_manager import dm


class Individual(object):
    id = 0

    def __init__(self, genotype):
        self.id = Individual.id
        Individual.id += 1
        self.genotype = genotype
        self.is_dominated = None
        self.tour_distance = self.calculate_tour_distance(self.genotype.city_ids)
        self.tour_cost = self.calculate_tour_cost(self.genotype.city_ids)

    def __repr__(self):
        return 'Individual ' + str(self.id) + ' with ' + repr(self.genotype)

    def __eq__(self, other):
        return self.id == other.id

    @staticmethod
    def calculate_tour_distance(city_ids):
        return sum(
            dm.get_distance(city_ids[i], city_ids[i + 1])
            for i in range(len(city_ids) - 1)
        )

    @staticmethod
    def calculate_tour_cost(city_ids):
        return sum(
            dm.get_cost(city_ids[i], city_ids[i + 1])
            for i in range(len(city_ids) - 1)
        )

    def get_gene(self, n):
        return self.genotype.city_ids[n]

    def dominates(self, other_individual):
        return (
            self.tour_distance <= other_individual.tour_distance and  # distance not worse
            self.tour_cost <= other_individual.tour_cost and  # cost not worse
            (
                self.tour_distance < other_individual.tour_distance or  # distance is better
                self.tour_cost < other_individual.tour_cost  # cost is better
            )
        )
