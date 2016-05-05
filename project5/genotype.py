import random
from data_manager import dm
import copy


class Genotype(object):
    def __init__(self, city_ids):
        self.city_ids = city_ids

    def __repr__(self):
        return 'Genotype ' + str(self.city_ids)

    def clone(self):
        return self.__class__(copy.deepcopy(self.city_ids))

    @staticmethod
    def get_random_genotype():
        city_ids = copy.deepcopy(dm.city_ids)
        random.shuffle(city_ids)
        return Genotype(city_ids)

    def mutate(self):
        random_city_id1, random_city_id2 = random.sample(dm.city_ids, 2)
        tmp = self.city_ids[random_city_id1]
        self.city_ids[random_city_id1] = self.city_ids[random_city_id2]
        self.city_ids[random_city_id2] = tmp
