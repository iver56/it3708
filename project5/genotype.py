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

    def crossover(self, other_genotype):
        len_gtype = len(self.city_ids)
        tmp_city_ids = [None for _ in range(len_gtype)]

        # random crossover interval
        interval = random.sample(range(0, len_gtype), 2)
        len_interval = ((len_gtype - interval[0]) + interval[1]) % len_gtype

        for i in range(interval[0], interval[0] + len_interval):
            i = i % len_gtype
            tmp_city_ids[i] = self.city_ids[i]

        for i in range(interval[1], interval[1] + 1 + len_gtype - len_interval):
            i = i % len_gtype
            for j in range(i, i + len_gtype):
                j = j % len_gtype
                if other_genotype.city_ids[j] not in tmp_city_ids:
                    tmp_city_ids[i] = other_genotype.city_ids[j]
                    break

        return tmp_city_ids
