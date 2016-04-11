import sys
import pygame
import world

pygame.display.init()


class Gfx(object):
    size = width, height = 1080, 540
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    RED = 230, 40, 40
    DARK_RED = 160, 20, 20
    GREEN = 20, 170, 20
    BLUE = 20, 120, 240

    def __init__(self, fps=100):
        self.GU_X = self.width / float(world.World.WIDTH)
        self.GU_Y = self.height / float(world.World.HEIGHT)

        self.screen = pygame.display.set_mode(self.size)

        self.clock = pygame.time.Clock()  # used for limiting the fps, so one can see each step
        self.fps = fps

    def draw_item(self, that_world):
        color = self.GREEN if that_world.item.width < that_world.agent.WIDTH else self.BLUE

        for x in range(that_world.item.x, that_world.item.x + that_world.item.width):
            rect = pygame.Rect(
                x * self.GU_X + 1,
                that_world.item.y * self.GU_Y + 1,
                self.GU_X - 2,
                self.GU_Y - 2
            )
            pygame.draw.rect(self.screen, color, rect)

    def draw_grid_lines(self, that_world):
        line_thickness = 1
        for y in range(that_world.HEIGHT):
            # rows
            pygame.draw.line(
                self.screen,
                self.BLACK,
                [0, y * self.GU_Y],
                [self.width, y * self.GU_Y],
                line_thickness
            )
        for x in range(that_world.WIDTH):
            # columns
            pygame.draw.line(
                self.screen,
                self.BLACK,
                [x * self.GU_X, 0],
                [x * self.GU_X, self.height],
                line_thickness
            )

    def draw_agent(self, that_world):
        for x in that_world.agent.get_occupied_x_positions():
            color = self.DARK_RED if that_world.is_shadowed(x) else self.RED
            rect = pygame.Rect(
                x * self.GU_X + 1,
                that_world.agent.y * self.GU_Y + 1,
                self.GU_X - 2,
                self.GU_Y - 2
            )
            pygame.draw.rect(self.screen, color, rect)

    def draw(self, that_world):
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

        self.draw_grid_lines(that_world)
        self.draw_item(that_world)
        self.draw_agent(that_world)

        pygame.display.flip()
