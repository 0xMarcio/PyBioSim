# Desc: Contains the parameters for the simulation
class SimulationParams:
    def __init__(self):
        self.grid_width = 100  # Width of the grid
        self.grid_height = 100  # Height of the grid
        self.initial_population = 20  # Starting number of creatures
        self.initial_energy = 100  # Initial energy for creatures
        self.max_energy = 300  # Maximum energy for creatures
        self.search_radius = 15  # Sensory radius for searching food
        self.regrowth_rate = 1  # Rate at which food regrows
        self.move_energy_cost = 1  # Energy cost for moving
        self.energy_gain_from_food = 50  # Energy gained from eating food
        self.mutation_rate = 0.1  # Mutation rate for genetic algorithm
        self.visualizer_width = 800  # Width of the visualizer window
        self.visualizer_height = 600  # Height of the visualizer window
        self.initial_genome = [0.5] * 8  # An example of initial genome weights
        self.num_steps = 250  # Number of steps to run the simulation
        self.reproductive_energy_threshold = 100  # Energy threshold for reproduction
        self.reproduction_cost = 50  # Energy cost for reproduction
        self.mate_selection_radius = 1  # Radius for mate selection
