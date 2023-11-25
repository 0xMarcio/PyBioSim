# This file contains the Genome class, which represents a genome in the population.
import random

class Genome:
    def __init__(self, genes):
        self.genes = genes  # A list representing the genome, where each gene could be a neural network weight

    def mutate(self, mutation_rate):
        # Apply mutations to the genome based on the mutation rate
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                # Apply a simple mutation: a small change to the gene
                mutation = random.choice([-1, 1]) * random.uniform(0.0, 0.1)
                self.genes[i] += mutation
                # Ensure the gene stays within some bounds, e.g., -1 to 1
                self.genes[i] = max(-1, min(self.genes[i], 1))

    def crossover(self, other_genome):
        """ Perform single-point crossover between self and other_genome """
        crossover_point = random.randint(1, len(self.genes) - 1)
        child_genes = self.genes[:crossover_point] + other_genome.genes[crossover_point:]
        return Genome(child_genes)

    def replicate_with_mutation(self):
        # Implement logic to replicate and mutate the genome
        # This can be as simple as copying the genome and applying random mutations
        # Or as complex as performing crossover with another genome
        new_genes = self.genes[:]  # Create a copy of the genes
        # Apply mutation logic here
        return Genome(new_genes)


# Example usage:
# parent_genome1 = Genome([0.5, -0.2, 0.1])
# parent_genome2 = Genome([-0.1, 0.3, -0.4])
# offspring_genome = Genome.crossover(parent_genome1, parent_genome2)
# offspring_genome.mutate(mutation_rate=0.05)
# print(offspring_genome.genes)
