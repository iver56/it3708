from boid import Boid
from gfx import Gfx


class Flock(object):
    instance = None

    def __init__(self):
        self.gfx = Gfx()
        self.boids = []
        for i in range(100):
            boid = Boid()
            self.boids.append(boid)
        Boid.all_boids = self.boids

        self.run()

    def run(self):
        while True:
            for boid in self.boids:
                boid.update()

            self.gfx.draw(self.boids)

if __name__ == '__main__':
    Flock.instance = Flock()
