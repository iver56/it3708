class Problem(object):
    @staticmethod
    def parse_args():
        pass

    @staticmethod
    def pre_run_hook():
        pass

    @staticmethod
    def post_run_hook(population):
        pass

    @staticmethod
    def calculate_fitness(individual):
        raise Exception('calculate_fitness must be implemented')
