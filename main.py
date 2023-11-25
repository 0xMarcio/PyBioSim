#!/usr/bin/env python3
import numpy as np
from config.params import SimulationParams
from environment.grid import Grid
from creatures.creature import Creature
from visualization.visualize import Visualizer
from simulation.sim import Simulation

def create_generation(genomes, params, grid):
    # Given a list of genomes, create a new generation of creatures
    # Each creature needs to be provided with a grid and params upon instantiation
    creatures = [Creature(genome, params.initial_energy, grid, params) for genome in genomes]
    return creatures

def reproduce_genomes(surviving_genomes, initial_population):
    new_genomes = []
    while len(new_genomes) < initial_population:
        for genome in surviving_genomes:
            if len(new_genomes) >= initial_population:
                break
            # Simple replication with mutation can be implemented here
            # For a more advanced approach, you can implement crossover between genomes
            new_genome = genome.replicate_with_mutation()
            new_genomes.append(new_genome)
    return new_genomes


def create_initial_genome(input_size, layer_sizes, output_size):
    # Create a random genome with weights for each layer in the neural network
    # The genome will be a list of weights for each layer
    genome = []
    previous_size = input_size

    # Initialize weights for each layer, including the output layer
    for layer_size in layer_sizes + [output_size]:
        # Initialize weights for this layer and flatten them into the genome list
        layer_weights = np.random.rand(previous_size * layer_size) * 2 - 1  # Random weights between -1 and 1
        genome.extend(layer_weights.tolist())
        previous_size = layer_size

    return genome

def main():
    params = SimulationParams()
    generations = 10  # Define how many generations you want to simulate

    # Initialize the grid for the first generation
    grid = Grid(params.grid_width, params.grid_height, params.regrowth_rate)

    # Example usage:
    input_size = 8  # Number of input neurons
    layer_sizes = [16, 8]  # Sizes of the hidden layers
    output_size = 4  # Number of output neurons

    # Create initial population of creatures
    initial_genomes = [create_initial_genome(input_size, layer_sizes, output_size) for _ in range(params.initial_population)]
    # initial_genomes = [params.initial_genome for _ in range(params.initial_population)]
    creatures = create_generation(initial_genomes, params, grid)

    for gen in range(generations):
        print(f"Generation {gen + 1} of {generations}")
        # Assign creatures to the grid
        grid.creatures = creatures

        # Initialize the visualizer
        visualizer = Visualizer(grid, creatures, width=params.visualizer_width, height=params.visualizer_height)

        # Run the simulation for the current generation
        simulation = Simulation(params, grid, creatures, visualizer)
        simulation.run()

        # Gather the genomes of the surviving creatures
        surviving_genomes = [creature.get_genome() for creature in simulation.creatures if creature.get_genome() is not None]

        # If no creatures survived, end the evolutionary process
        if len(surviving_genomes) == 0:
            print(f"All creatures have died in generation {gen}. Ending the evolutionary process.")
            break

        # Reproduce genomes to meet the initial population requirement
        new_genomes = reproduce_genomes(surviving_genomes, params.initial_population)

        # Reinitialize the grid for the next generation
        grid = Grid(params.grid_width, params.grid_height, params.regrowth_rate)

        # Create the next generation of creatures from the new genomes
        creatures = create_generation(new_genomes, params, grid)


if __name__ == "__main__":
    main()
