import csv


class DataManager(object):
    def __init__(self):
        self.cost_matrix = self.read_csv('cost.csv')
        self.distance_matrix = self.read_csv('distance.csv')
        self.num_cities = len(self.cost_matrix)
        self.city_ids = range(self.num_cities)

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

        # remove first row and first column, because they contain city ids
        rows.pop(0)
        for row in rows:
            row.pop(0)

        return rows

    def get_cost(self, city1_id, city2_id):
        if city2_id > city1_id:  # Avoid empty part of the lower triangular matrix
            return self.cost_matrix[city2_id][city1_id]
        return self.cost_matrix[city1_id][city2_id]

    def get_distance(self, city1_id, city2_id):
        if city2_id > city1_id:  # Avoid empty part of the lower triangular matrix
            return self.distance_matrix[city2_id][city1_id]
        return self.distance_matrix[city1_id][city2_id]

dm = DataManager()
