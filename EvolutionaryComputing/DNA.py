import random

class DNA():
    def __init__(self, length, mutation_factor):
        self.length = length
        self.mutation_factor = mutation_factor
        self.genes = []
        for _ in range(length):
            self.genes.append(self.select_random_character())
        self.score = 0

    def get_phrase(self):
        """
        Get string of the phrase
        """
        return ''.join(self.genes)

    def fitness_score(self, target: list):
        """
        Computes a score based on how close to the target we are.

        Args:
            - target: the target object, in this example another sequence of characters
        """
        score = 0
        for i in range(self.length):
            if target[i] == self.genes[i]:
                score += 1
        
        self.score = score / self.length

    def crossover(self, partner):
        """
        Applies crossover to create the child for the next generation.
        The new sentence will be created by using half of both parents sentence.

        Args:
            - partner: has to be another DNA object.

        Returns a new object containing the child
        """
        child = DNA(self.length, self.mutation_factor)

        half = self.length // 2
        new_genes = self.genes[:half] + partner.genes[half:]
        child.genes = new_genes

        return child

    def mutate(self):
        """
        Applies mutation, i.e. a character randomly changes
        """
        for i in range(self.length):
            if random.randint(0, 100) < self.mutation_factor:
                self.genes[i] = self.select_random_character()
                break

    def select_random_character(self):
        """
        Return a lower letter character
        """
        rand = random.randint(1, 27)
        if rand == 27:
            return " "
        start = ord('A') - 1
        char = chr(start + rand)
        return char