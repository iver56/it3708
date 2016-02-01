import object_collection
import boid
import predator
import obstacle
import gfx


class Flock(object):
    instance = None

    def __init__(self):
        self.gfx = gfx.Gfx()
        object_collection.ObjectCollection.all_boids = []
        for i in range(100):
            object_collection.ObjectCollection.all_boids.append(boid.Boid())

        object_collection.ObjectCollection.all_predators = []
        for i in range(0):
            object_collection.ObjectCollection.all_predators.append(predator.Predator())

        self.run()

    def run(self):
        while True:
            for dat_boid in object_collection.ObjectCollection.all_boids:
                dat_boid.update()

            for dat_predator in object_collection.ObjectCollection.all_predators:
                dat_predator.update()

            self.gfx.draw()

if __name__ == '__main__':
    Flock.instance = Flock()
