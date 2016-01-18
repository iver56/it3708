from boid import Boid
from gfx import Gfx
from object_collection import ObjectCollection
from predator import Predator


class Flock(object):
    instance = None

    def __init__(self):
        self.gfx = Gfx()
        ObjectCollection.all_boids = []
        for i in range(100):
            boid = Boid()
            ObjectCollection.all_boids.append(boid)

        ObjectCollection.all_predators = []
        for i in range(2):
            predator = Predator()
            ObjectCollection.all_predators.append(predator)

        self.run()

    def run(self):
        while True:
            for boid in ObjectCollection.all_boids:
                boid.update()

            for predator in ObjectCollection.all_predators:
                predator.update()

            self.gfx.draw()

if __name__ == '__main__':
    Flock.instance = Flock()
