from data_manager import dm


class Individual(object):
    id = 0

    def __init__(self, genotype):
        self.id = Individual.id
        Individual.id += 1
        self.genotype = genotype
        self.tour_distance = self.calculate_tour_distance(self.genotype.city_ids)
        self.tour_cost = self.calculate_tour_cost(self.genotype.city_ids)

        # fields used in crowding distance method
        self.objectives = (self.tour_distance, self.tour_cost)
        self.crowding_distance = 0

        # the following fields are used in the fast_non_dominated_sort method
        self.individuals_dominated = None  # the set of individuals that are dominated by this individual  # TODO: this variable may be moved to fast_non_dominated_sort, as it is temporary
        self.domination_counter = None  # the number of individuals that dominate this individual
        self.rank = None

    def __repr__(self):
        return 'Individual ' + str(self.id) + ' with ' + repr(self.genotype)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

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

    def set_crowding_distance(self, d):
        self.crowding_distance = d

    def dominates(self, other_individual):
        return (
            self.tour_distance <= other_individual.tour_distance and  # distance not worse
            self.tour_cost <= other_individual.tour_cost and  # cost not worse
            (
                self.tour_distance < other_individual.tour_distance or  # distance is better
                self.tour_cost < other_individual.tour_cost  # cost is better
            )
        )

    def calculate_crowding_distance(self, i, pareto_front, max_dist, min_dist, objective):
        self.crowding_distance += \
            (pareto_front[i + 1].objectives[objective] - pareto_front[i - 1].objectives[objective]) / \
            (max_dist - min_dist)
