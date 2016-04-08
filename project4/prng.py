import random


class Prng(object):
    def __init__(self, seed):
        random.seed(seed)
        self.state = random.getstate()

    def randint(self, a, b):
        random.setstate(self.state)
        result = random.randint(a, b)
        self.state = random.getstate()
        return result

    def random(self):
        random.setstate(self.state)
        result = random.random()
        self.state = random.getstate()
        return result
