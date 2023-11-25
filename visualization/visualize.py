# This file contains the Grid class which represents the environment in which the creatures live.
import pygame

# Define some color constants for drawing
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_RED = (255, 128, 128)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 255, 255)
PURPLE = (128, 0, 128)
PINK = (255, 0, 255)
ORANGE = (255, 165, 0)
BROWN = (165, 42, 42)
WHITE = (255, 255, 255)

class Visualizer:
    def __init__(self, grid, creatures, width=800, height=600):
        """ Initialize the Pygame window and set up the grid """
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.grid = grid
        self.creatures = creatures  # Add this line to store the creatures
        self.cell_width = width // grid.width
        self.cell_height = height // grid.height
        self.width = width
        self.height = height

    def draw_grid(self):
        """ Draw the grid lines """
        for x in range(0, self.width, self.cell_width):
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_height):
            pygame.draw.line(self.screen, BLACK, (0, y), (self.width, y))

    def draw_cells(self):
        """ Draw the cells based on the grid's state """
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                rect = pygame.Rect(x * self.cell_width, y * self.cell_height, self.cell_width, self.cell_height)
                if self.grid.get_cell(x, y) == 1:  # Food
                    pygame.draw.rect(self.screen, GREEN, rect)
                elif self.grid.get_cell(x, y) == 2:  # Creature
                    pygame.draw.rect(self.screen, ORANGE, rect)
                    print("Creature at", x, y)
                    # pygame.draw.rect(self.screen, RED, rect)

    def draw_creatures(self):
        """ Draw creatures on the grid, with newborn creatures in purple """
        for creature in self.creatures:
            if creature.alive:
                x_center = creature.x * self.cell_width + self.cell_width // 2
                y_center = creature.y * self.cell_height + self.cell_height // 2
                # if creature.newborn:
                #     if creature.gender is 'female':
                #         color = PINK
                #     else:
                #         color = PURPLE
                # else:
                #     if creature.gender is 'female':
                #         color = RED
                #     else:
                #         color = BLUE
                if creature.gender is 'female':
                    color = RED
                else:
                    color = BLUE

                pygame.draw.circle(self.screen, color, (x_center, y_center), self.cell_width // 2)

    def draw(self):
        """ Draw the entire scene: the grid and the creatures """
        self.screen.fill(BLACK)  # Clear the screen
        self.draw_grid()
        self.draw_cells()
        self.draw_creatures()  # Add this line to draw the creatures
        pygame.display.flip()  # Update the full display

    def handle_events(self):
        """ Handle Pygame events like window closing """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 'quit'

    def close(self):
        """ Clean up and close the Pygame window """
        pygame.quit()

