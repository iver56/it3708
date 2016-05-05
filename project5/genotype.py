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

    def crossover(self, other):
        tmp_city_ids = [None for i in range(len(self.city_ids))]

        # Random crossover interval
        interval = random.sample(range(0, len(self.city_ids)), 2)
        print "Interval", interval

        len_interval = max(interval) - min(interval) % len(tmp_city_ids)

        counter = 0
        i = min(interval)
        while counter < len_interval:
            tmp_city_ids[i] = self.city_ids[i]

            i = (i + 1) % len(tmp_city_ids)
            counter += 1

        print tmp_city_ids
        print

        # Good to here.

        len_not_interval = len(tmp_city_ids) - len_interval
        print len_not_interval
        i = max(interval) + 1
        indexer = (max(interval) + 1) % len(tmp_city_ids)
        counter = 0
        while counter < len_not_interval - 1:
            if other.get_gene(indexer) not in tmp_city_ids:
                tmp_city_ids[i] = other.get_gene(indexer)

                i = (i + 1) % len(tmp_city_ids)
                counter += 1
                indexer = (indexer + 1) % len(tmp_city_ids)
            else:
                #i = (i + 1) % len(tmp_city_ids)
                indexer = (indexer + 1) % len(tmp_city_ids)

        print tmp_city_ids
        return tmp_city_ids
#len_interval = (interval[0] - interval[1]) % len(tmp_city_ids)
