# This file contains the Peeps class, which is the main class for the creatures in the simulation.
from environment.grid import Grid
from creatures.creature import Creature
from visualization.visualize import Visualizer
from config.params import SimulationParams

class Simulation:
    def __init__(self, params, grid, creatures, visualizer):
        self.params = params
        self.grid = grid
        self.creatures = creatures
        self.visualizer = visualizer
        self.current_step = 0

    def step(self):
        # Update the environment
        self.grid.update()

        # Let creatures act and reproduce
        for creature in self.creatures:
            creature.act()
            if creature.energy > self.params.reproductive_energy_threshold:
                offspring = creature.reproduce()
                if offspring:
                    self.creatures.append(offspring)

        # Remove dead creatures
        self.creatures = [creature for creature in self.creatures if creature.alive]

        # Update visualization; no need to pass creatures or grid since Visualizer has access to them
        self.visualizer.draw()

        # Increment step count
        self.current_step += 1
        if self.current_step % 100 == 0:
            print("Step:", self.current_step)
            print("Population:", len(self.creatures))

    def run(self):
        while not self.check_end_conditions():
            self.step()
            self.visualizer.creatures = self.creatures  # Update the creatures in the visualizer
            if self.visualizer.handle_events() == 'quit':
                break
        self.end_simulation()

    def check_end_conditions(self):
        # Define conditions that will end the simulation
        return len(self.creatures) == 0 or self.current_step >= self.params.num_steps

    def end_simulation(self):
        # Handle the end of the simulation
        print("Simulation ended at step", self.current_step)
        self.visualizer.close()

# Example usage:
# params = SimulationParams()
# grid = Grid(params.grid_width, params.grid_height, params.regrowth_rate)
# creatures = [Creature(params.genome, params.start_energy, grid) for _ in range(params.initial_population)]
# visualizer = Visualizer(grid, creatures)
# simulation = Simulation(params, grid, creatures, visualizer)
# simulation.run()
