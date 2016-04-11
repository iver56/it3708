import sys, pygame
from grid import Grid, Item

pygame.display.init()


class Gfx(object):
    size = width, height = 540, 540
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    RED = 230, 40, 40
    GREEN = 20, 170, 20

    def __init__(self, fps=100):
        self.GU_X = self.width / float(Grid.WIDTH)
        self.GU_Y = self.height / float(Grid.HEIGHT)

        self.screen = pygame.display.set_mode(self.size)

        self.clock = pygame.time.Clock()  # used for limiting the fps, so one can see each step
        self.fps = fps

        self.agent_sprite = pygame.image.load("agent.png")

    def draw_items(self, grid):
        for i in range(len(grid.cells)):
            if grid.cells[i] != Item.Nothing:
                x, y = grid.convert_1d_to_2d(i)
                color = self.GREEN if grid.cells[i] == Item.Food else self.RED
                self.draw_item(x, y, color)

    def draw_item(self, x, y, color):
        rect = pygame.Rect(
            x * self.GU_X + 1,
            y * self.GU_Y + 1,
            self.GU_X - 2,
            self.GU_Y - 2
        )
        pygame.draw.rect(self.screen, color, rect)

    def draw_grid_lines(self, grid):
        line_thickness = 1
        for y in range(grid.n):
            pygame.draw.line(
                self.screen,
                self.BLACK,
                [0, y * self.GU_Y],
                [self.width, y * self.GU_Y],
                line_thickness
            )
        for x in range(grid.n):
            pygame.draw.line(
                self.screen,
                self.BLACK,
                [x * self.GU_X, 0],
                [x * self.GU_X, self.height],
                line_thickness
            )

    def draw_agent(self, agent):
        self.screen.blit(
            pygame.transform.rotate(self.agent_sprite, agent.direction),
            (
                agent.x * self.GU_X - 12,
                agent.y * self.GU_Y - 12,
                agent.x * self.GU_X + self.GU_X + 12,
                agent.y * self.GU_Y + self.GU_Y + 12
            )
        )

    def draw(self, grid, agent):
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

        self.draw_grid_lines(grid)
        self.draw_items(grid)
        self.draw_agent(agent)

        pygame.display.flip()
