import torch
import random
from neuralnet.neuralnet import NeuralNetwork
from genome.genome import Genome

class Creature:
    def __init__(self, genome, energy, grid, params):
        self.genome = Genome(genome) if isinstance(genome, list) else genome
        self.energy = energy
        self.grid = grid
        self.params = params  # Store the simulation parameters
        self.x = random.randint(0, grid.width - 1)
        self.y = random.randint(0, grid.height - 1)
        self.neural_network = NeuralNetwork(input_size=8, hidden_layers=[16, 8], output_size=4)
        self.newborn = False
        self.alive = True
        self.gender = random.choice(['male', 'female'])

    def act(self):
        # Look for food with each move
        food_direction = self.detect_food_direction(self.params.search_radius)
        if food_direction != [0, 0]:  # If there's food detected in a direction
            self.move_towards(food_direction)
        else:
            # If no food is detected, either move randomly or stay still to conserve energy
            if random.random() < 0.1:  # 10% chance to move randomly
                self.move(random.choice([0, 1, 2, 3]))
            else:
                pass  # Stay still

        # After moving, decrease energy and check for death
        self.energy -= self.params.move_energy_cost
        if self.energy <= 0:
            self.alive = False

        # If the creature is on a food source, eat it
        if self.grid.get_cell(self.x, self.y) == 1:
            self.eat()

    def detect_food_direction(self, search_radius):
        direction_vector = [0, 0]
        min_distance = float('inf')

        # Iterate through the grid within the search radius
        for dy in range(-search_radius, search_radius + 1):
            for dx in range(-search_radius, search_radius + 1):
                nx, ny = self.x + dx, self.y + dy
                # Check if this grid position is within bounds
                if (0 <= nx < self.grid.width and 0 <= ny < self.grid.height):
                    # Check if the current cell has food
                    if self.grid.get_cell(nx, ny) == 1:
                        distance = (dx**2 + dy**2)**0.5
                        if distance < min_distance:
                            min_distance = distance
                            direction_vector = [dx, dy]

        # Normalize the direction vector if a non-zero vector was found
        if min_distance < float('inf') and min_distance > 0:
            norm = (direction_vector[0]**2 + direction_vector[1]**2)**0.5
            direction_vector = [direction_vector[0] / norm, direction_vector[1] / norm]

        return direction_vector  # This should only have two elements now

    def move_towards(self, direction_vector):
        # Translate the food direction into a movement action
        dx, dy = direction_vector
        if abs(dx) > abs(dy):  # Move in x direction
            self.move(1 if dx > 0 else 3)  # Right if dx positive, left if dx negative
        else:  # Move in y direction
            self.move(2 if dy > 0 else 0)  # Down if dy positive, up if dy negative

    def move(self, direction):
        # Update the creature's position based on the direction
        if direction == 0 and self.y > 0:  # Up
            self.y -= 1
        elif direction == 1 and self.x < self.grid.width - 1:  # Right
            self.x += 1
        elif direction == 2 and self.y < self.grid.height - 1:  # Down
            self.y += 1
        elif direction == 3 and self.x > 0:  # Left
            self.x -= 1

    def get_sensor_input(self, food_direction):
        # Construct the sensor input with the food direction and current energy
        sensor_input = [self.energy / self.params.max_energy] + food_direction

        # Pad with zeros to create an 8-element vector
        sensor_input.extend([0] * (8 - len(sensor_input)))
        return torch.tensor([sensor_input], dtype=torch.float32)

    def eat(self):
        # Logic to consume food and gain energy
        self.energy += self.params.energy_gain_from_food
        # Assuming food is consumed and removed from the grid
        self.grid.set_cell(self.x, self.y, 0)

    def find_mate(self):
        potential_mates = self.grid.get_creatures_within_radius(self.x, self.y, self.params.mate_selection_radius)
        potential_mates = [mate for mate in potential_mates if mate.energy > self.params.reproductive_energy_threshold]
        potential_mates = [mate for mate in potential_mates if mate.gender != self.gender]
        return random.choice(potential_mates) if potential_mates else None

    def reproduce(self):
        if self.energy > self.params.reproductive_energy_threshold:
            mate = self.find_mate()
            if mate and mate != self:
                # Ensure that we're using the crossover method of the Genome instance
                child_genome = self.genome.crossover(mate.genome)
                # Mutate the offspring's genome
                child_genome.mutate(self.params.mutation_rate)
                # Create a new creature with the offspring's genome
                child = Creature(child_genome, self.params.initial_energy, self.grid, self.params)
                # Reduce parents' energy due to the cost of reproduction
                self.energy -= self.params.reproduction_cost
                mate.energy -= self.params.reproduction_cost
                child.newborn = True  # Indicate that the creature is newborn
                return child
        return None

    def get_genome(self):
        # Returns the creature's genome if it's alive
        return self.genome if self.alive else None
