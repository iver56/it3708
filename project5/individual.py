from data_manager import dm


class Individual(object):
    def __init__(self, genotype):
        self.genotype = genotype

    def calculate_tour_distance(self):
        distance = 0
        for i in range(len(self.genotype.city_ids) - 1):
            distance += dm.get_distance(i, i + 1)
        return distance
