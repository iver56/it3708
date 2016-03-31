import sys, pygame

pygame.display.init()


class Gfx(object):
    size = width, height = 540, 540
    WHITE = 255, 255, 255  # undiscovered tiles
    BLACK = 0, 0, 0  # closed tiles

    def __init__(self, grid, fps=10):
        self.grid = grid

        self.GU_X = self.width / float(grid.n)
        self.GU_Y = self.height / float(grid.n)

        self.screen = pygame.display.set_mode(self.size)

        self.clock = pygame.time.Clock()  # used for limiting the fps, so one can see each step
        self.fps = fps

    def draw_tile(self, x, y, color):
        rect = pygame.Rect(
            x * self.GU_X + 1,
            y * self.GU_Y + 1,
            self.GU_X - 2,
            self.GU_Y - 2
        )
        pygame.draw.rect(self.screen, color, rect)

    def draw_grid(self):
        line_thickness = 2
        for y in range(self.grid.n):
            pygame.draw.line(
                self.screen,
                self.BLACK,
                [0, y * self.GU_Y],
                [self.width, y * self.GU_Y],
                line_thickness
            )
        for x in range(self.grid.n):
            pygame.draw.line(
                self.screen,
                self.BLACK,
                [x * self.GU_X, 0],
                [x * self.GU_X, self.height],
                line_thickness
            )

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.fps /= 2  # halve the fps
                if event.key == pygame.K_UP:
                    self.fps *= 2  # double the fps
                    if self.fps > 256.0:
                        self.fps = 256.0

        self.clock.tick(self.fps)

        self.screen.fill(self.WHITE)

        self.draw_grid()

        pygame.display.flip()
