import csv


class DataManager(object):
    def __init__(self):
        self.cost_matrix = self.read_csv('cost.csv')
        self.distance_matrix = self.read_csv('distance.csv')

    @staticmethod
    def read_csv(csv_filename):
        """
        Returns a lower triangular matrix (a list of lists)
        """
        rows = []
        with open(csv_filename, 'rb') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                row = map(lambda x: None if len(x) == 0 else int(x), row)
                rows.append(row)
        return rows

    def get_cost(self, city1_id, city2_id):
        if city1_id == 0 or city2_id == 0:
            raise ValueError('city id cannot be zero')
        if city2_id > city1_id:  # Avoid empty part of the lower triangular matrix
            return self.cost_matrix[city2_id][city1_id]
        return self.cost_matrix[city1_id][city2_id]

    def get_distance(self, city1_id, city2_id):
        if city1_id == 0 or city2_id == 0:
            raise ValueError('city id cannot be zero')
        if city2_id > city1_id:  # Avoid empty part of the lower triangular matrix
            return self.distance_matrix[city2_id][city1_id]
        return self.distance_matrix[city1_id][city2_id]

    def get_num_cities(self):
        return len(self.cost_matrix) - 1

dm = DataManager()
