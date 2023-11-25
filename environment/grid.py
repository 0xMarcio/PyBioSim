# This file contains the Grid class which represents the environment in which the creatures live.
import numpy as np

class Grid:
    def __init__(self, width, height, regrowth_rate):
        self.width = width
        self.height = height
        self.cells = np.zeros((height, width), dtype=np.uint8)
        self.regrowth_rate = regrowth_rate  # The rate at which food regrows
        self.creatures = []  # This will be populated with Creature instances

    def update(self):
        # Regenerate food randomly based on the regrowth rate
        for _ in range(self.regrowth_rate):
            x, y = np.random.randint(0, self.width), np.random.randint(0, self.height)
            self.cells[y, x] = 1  # Assume 1 represents food

    def get_cell(self, x, y):
        return self.cells[y % self.height, x % self.width]

    def set_cell(self, x, y, value):
        self.cells[y % self.height, x % self.width] = value

    def add_food(self, amount):
        for _ in range(amount):
            x, y = np.random.randint(0, self.width), np.random.randint(0, self.height)
            self.cells[y, x] = 1  # Let's say 1 represents food

    def consume_food(self, x, y):
        if self.cells[y, x] == 1:
            self.cells[y, x] = 0  # Remove food from the grid
            return True
        return False

    def get_info_at(self, x, y):
        return self.cells[y % self.height, x % self.width]

    def get_creatures_within_radius(self, x, y, radius):
        # Return a list of creatures within the specified radius of the (x, y) coordinates
        creatures_within_radius = []
        for creature in self.creatures:
            if creature.alive:
                distance = np.sqrt((creature.x - x) ** 2 + (creature.y - y) ** 2)
                if distance <= radius:
                    creatures_within_radius.append(creature)
        return creatures_within_radius

    def update_creatures(self):
        # Update creatures on the grid for the new turn
        for creature in self.creatures:
            if creature.alive:
                self.cells[creature.y, creature.x] = 2  # Assume 2 represents a creature
            else:
                self.cells[creature.y, creature.x] = 0  # Clear the dead creature

# Please note that this is a simplified version of the grid. Additional features and complexity
# can be added depending on the needs of your simulation.
