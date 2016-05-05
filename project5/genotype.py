import random
from data_manager import dm


class Genotype(object):
    def __init__(self, city_ids):
        self.city_ids = city_ids

    def __repr__(self):
        return 'Genotype ' + str(self.city_ids)

    @staticmethod
    def get_random_genotype():
        num_cities = dm.get_num_cities()
        city_ids = range(1, num_cities + 1)
        random.shuffle(city_ids)
        return Genotype(city_ids)
